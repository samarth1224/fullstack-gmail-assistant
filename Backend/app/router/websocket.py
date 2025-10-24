from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlmodel import Session, select

from Backend.Database.conversation import Conversation
from Backend.Database.database import get_session
from Backend.Database.messages import Message
from Backend.Database.Users import User
from agent.runner import call_agent_async, create_session, runner
from ..dependecies import verify_user

VerifyUserDep = Annotated[User, Depends(verify_user)]
SessionDep = Annotated[Session,  Depends(get_session)]
router = APIRouter(prefix='/ws')



@router.websocket("/{conversationid}")
async def message(session:SessionDep, websocket: WebSocket,conversationid: str):
    await websocket.accept()
    user_id = session.exec(select(Conversation.user_id).where(Conversation.conversation_id == conversationid)).first()
    

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
                                   websocket=websocket,
                                   session=session)
    except WebSocketDisconnect:
        print(f"Client disconnected from {conversationid}")
