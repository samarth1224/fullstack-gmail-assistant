# Handles user login.

import base64
import json
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from google.auth.transport import requests
from google.oauth2 import id_token
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from sqlmodel import Session,select
from starlette.responses import RedirectResponse

from dotenv import load_dotenv

from ..Database.database import get_session
from ..Database.Users import User

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI', "http://127.0.0.1:8005/auth/callback")
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID') # For token verification
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET') # For OAuth flow

SessionDep = Annotated[Session,  Depends(get_session)]



router = APIRouter(prefix='/auth')


@router.get('/login')
async def login():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth client ID or secret not configured.")
    client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": os.getenv('AUTH_URI'),
                "token_uri": os.getenv('TOKEN_URI'),
                "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url')
            }
        }

      
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI

    authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

    return RedirectResponse(authorization_url)

@router.get('/callback')
async def callback(request: Request,response: Response, session: SessionDep):
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth client ID or secret not configured.")

    try:
        client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": os.getenv('AUTH_URI'),
                    "token_uri": os.getenv('TOKEN_URI'),
                    "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url')
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URI

        flow.fetch_token(code= request.query_params.get('code'))

        credential = flow.credentials
        print(credential)

    except Exception as e:
        raise(HTTPException(status_code=400, detail=f"Token exchange failed {e}"))

    response.set_cookie(key = 'token', value=credential.id_token,httponly=True,samesite="None",secure=True)
    
    try:
        user_info_dict = id_token.verify_oauth2_token(credential.id_token, requests.Request(), GOOGLE_CLIENT_ID)

     
        statement = select(User).where(User.sub == user_info_dict['sub'])
        db_user = session.exec(statement).first()

        if db_user:

            print("User already in database. Updating tokens.")
            db_user.access_token = credential.token
     
            if credential.refresh_token:
                db_user.refresh_token = credential.refresh_token
            session.add(db_user)
            user_to_return = db_user
        else:
         
            print("Creating new user in database.")
            new_user = User(
                sub=user_info_dict['sub'],
                emailid=user_info_dict['email'],
                username=user_info_dict.get('name', 'N/A'), 
                access_token=credential.access_token,
                refresh_token=credential.refresh_token
            )
            session.add(new_user)
            user_to_return = new_user

        session.commit()
        session.refresh(user_to_return)

    except Exception as e:
        session.rollback() 
        raise HTTPException(status_code=400, detail=f"Failed to verify token or save user: {e}")

    return user_to_return


