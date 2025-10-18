from fastapi import APIRouter, WebSocket, WebSocketDisconnect,Depends
from agent.runner import call_agent_async, runner, create_session
from ..dependecies import verify_user
from ..Database.database import get_session
from ..Database.messages import Message,MessagePublic
from ..Database.conversation import  Conversation
from ..Database.Users import User
from ..Database.database import get_session,Session
from typing import Annotated
from datetime import datetime
from sqlmodel import Session,select

VerifyUserDep = Annotated[User, Depends(verify_user)]
SessionDep = Annotated[Session,  Depends(get_session)]
router = APIRouter(prefix='/ws')

# async def create_session(user_id,conversation_id):
#     return await session_service.create_session(app_name=APP_NAME,
#                                                 user_id=user_id,
#                                                 session_id=conversation_id)

@router.websocket("/{conversationid}")
async def message(session:SessionDep, websocket: WebSocket,conversationid: str):
    await websocket.accept()
    user_id = session.exec(select(Conversation.user_id).where(Conversation.conversation_id == conversationid)).first()
    print("websocket intial")

    try:
        while True:
            data = await websocket.receive_text()
            message_dict = {
                "conversation_id": conversationid,
                "user_id": user_id,
                "message_content": data,
                "send_time": datetime.utcnow(),
                'message_type':'user'
            }
            message = Message.model_validate(message_dict)
            session.add(message)
            session.commit()
            session.refresh(message)

            await call_agent_async(prompt=data,
                                   runner=runner,
                                   user_id=user_id,
                                   session_id=conversationid,
                                   websocket=websocket)
    except WebSocketDisconnect:
        print(f"Client disconnected from {conversationid}")
