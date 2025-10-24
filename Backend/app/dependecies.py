from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Request
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlmodel import Session, select
import os

from dotenv import load_dotenv

from .Database.database import get_session
from .Database.Users import User

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
async def verify_user(request: Request,session: Annotated [Session,Depends(get_session)] ,token: str =  Cookie(None)):
    '''
    Dependecy to check user auth status.
    '''
    print('I ')
    print(token)
    print(request.cookies)

    try:
        id_info = id_token.verify_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        sub = id_info['sub']
        print(sub)
    except:
        raise HTTPException(status_code=401,detail='user not logged in!')
    user = session.exec(select(User).where(User.sub == sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not logged in or needs to sign up!")
    return user
