# Handles user login.

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from fastapi import FastAPI,Request,Cookie,Depends,Response,APIRouter
from ..Database.Users import User, UserPublic
from ..Database.database import get_session
from sqlmodel import Session
from typing import Annotated
from starlette.responses import RedirectResponse
import base64
import json


from google.oauth2 import id_token
from google.auth.transport import requests


REDIRECT_URI = "http://127.0.0.1:8005/auth/callback"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
GOOGLE_CLIENT_ID = '635938163535-8a3sug2kct2hbq94hi4dp9j0n0qit12b.apps.googleusercontent.com'
SessionDep = Annotated[Session,  Depends(get_session)]



router = APIRouter(prefix='/auth')


@router.get('/login')
async def login():

    flow = Flow.from_client_secrets_file(client_secrets_file='D:\Projects\GMAIL-Agent\credentials.json',
                                         scopes=SCOPES,
                                         redirect_uri=REDIRECT_URI)
    authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

    return RedirectResponse(authorization_url)

@router.get('/callback')
async def callback(request: Request,response: Response, session: SessionDep):
    try:
        flow = Flow.from_client_secrets_file(client_secrets_file='D:\Projects\GMAIL-Agent\credentials.json',
                                         scopes=SCOPES,
                                         redirect_uri=REDIRECT_URI)

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


