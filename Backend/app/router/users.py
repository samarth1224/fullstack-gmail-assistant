# 'users'  route.
import datetime
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select

from agent.runner import create_session
from ..dependecies import verify_user
from ..Database.conversation import Conversation, ConversationPublic
from ..Database.database import get_session
from ..Database.messages import Message
from ..Database.Users import User, UserPublic


SessionDep = Annotated[Session,  Depends(get_session)]
VerifyUserDep = Annotated[User, Depends(verify_user)]

router  = APIRouter(prefix='/users')


@router.get('/',response_model=UserPublic)
async def users(user : VerifyUserDep,request: Request):
    print(request.cookies)
    return user

@router.get('/websocket',response_model=UserPublic)
def get_websocket_token(user : VerifyUserDep):
    '''this function checks if its the genuine user or not and than generates a random ID
    sends this to server which uses it for securly connecting with websocket.'''
    return user

@router.get('/conversations', response_model= list[ConversationPublic])
async def conversations(session: SessionDep, user: VerifyUserDep): 
    conversation = session.exec(select(Conversation).where(Conversation.user_id == user.user_id ))
    return conversation

@router.get('/messages/{conversation_id}', response_model=list[MessagePublic])
async def messages(conversation_id: uuid4, session: SessionDep,user: VerifyUserDep):
    message = session.exec(select(Message).where((Message.conversation_id == conversation_id),(Message.user_id == user.user_id))).all()
    if message:
        return message
    else:
        raise HTTPException(status_code=403,detail='You are not authorized to view this conversation or it does not exist!')

@router.post('/newconversation')
async def add_new_conversation(session: SessionDep,user: VerifyUserDep):
    conversation_dict = {
        "conversation_name": "New Conversation",  # required
          # optional, defaults to utcnow()
        "user_id": user.user_id # replace with actual user UUID
    }
    new_conversation = Conversation.model_validate(conversation_dict)
    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    print(new_conversation.conversation_id)
    await create_session(user_id=user.user_id, conversation_id= new_conversation.conversation_id)

    return {"conversation_id": str(new_conversation.conversation_id)}





