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
from sqlmodel import Session
from starlette.responses import RedirectResponse

from dotenv import load_dotenv

from ..Database.database import get_session
from ..Database.Users import User

load_dotenv()

REDIRECT_URI = os.getenv('REDIRECT_URI', "http://127.0.0.1:8005/auth/callback")
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID') # For token verification
CLIENT_ID_RAW = os.getenv('GOOGLE_CLIENT_ID_RAW') # For OAuth flow
CLIENT_SECRET_RAW = os.getenv('GOOGLE_CLIENT_SECRET_RAW') # For OAuth flow

SessionDep = Annotated[Session,  Depends(get_session)]



router = APIRouter(prefix='/auth')


@router.get('/login')
async def login():
    if not CLIENT_ID_RAW or not CLIENT_SECRET_RAW:
        raise HTTPException(status_code=500, detail="Google OAuth client ID or secret not configured.")

    client_config = {
        "web": {
            "client_id": CLIENT_ID_RAW,
            "client_secret": CLIENT_SECRET_RAW,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
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
    if not CLIENT_ID_RAW or not CLIENT_SECRET_RAW:
        raise HTTPException(status_code=500, detail="Google OAuth client ID or secret not configured.")

    try:
        client_config = {
            "web": {
                "client_id": CLIENT_ID_RAW,
                "client_secret": CLIENT_SECRET_RAW,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        flow.redirect_uri = REDIRECT_URI

        flow.fetch_token(code= request.query_params.get('code'))

        credential = flow.credentials
    except Exception as e:
        raise(HTTPException(status_code=400, detail="Token exchange failed"))

    response.set_cookie(key = 'token', value=credential.id_token,httponly=True,samesite="None",secure=True)
    try:
        user_info = id_token.verify_token(credential.id_token,requests.Request(), GOOGLE_CLIENT_ID)
        user_info = {'username':"samarth" ,'emailid': user_info['email'],'sub':user_info['sub'] }
    except Exception as e:
        raise (HTTPException(status_code=400, detail="failed to verify token"))
    new_user = User.model_validate(user_info)
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except :
        print('user already in database')

    return new_user


