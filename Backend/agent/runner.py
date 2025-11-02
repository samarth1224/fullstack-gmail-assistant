import json
from datetime import datetime
from typing import Annotated
import os

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from google.adk.auth import AuthConfig
from google.adk.events import Event, EventActions

from app.Database.conversation import Conversation
from app.Database.database import get_session
from app.Database.messages import Message
from app.Database.Users import User, UserPublic
from sqlmodel import Session,select,update

from .agent import root_agent

import json
import time
from dotenv import load_dotenv
 

load_dotenv()
REDIRECT_URI = os.getenv('REDIRECT_URI', "http://127.0.0.1:8005/auth/callback")

APP_NAME = "gmail_agent"

dbsession = next(get_session()) 

session_service = DatabaseSessionService(
    db_url=os.getenv('DATABASE_URL')
)
runner = Runner(app_name=APP_NAME,
                session_service=session_service,
                agent=root_agent)


async def create_session(user_id,conversation_id):
    return await session_service.create_session(app_name=APP_NAME,
                                                user_id=str(user_id),
                                                session_id=str(conversation_id),
                                                state={'conv_name':'New Conversation'})

async def call_agent_async(prompt: str,runner, user_id, session_id, websocket):

    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_response_text = "Agent did not produce a final response."
    response = {'response_type':'final',
                'content':{'message':final_response_text}
                }

    async for event in runner.run_async(user_id=str(user_id), session_id=str(session_id), new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                response['content']['message']= event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                response['content']['message'] = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

        for call in event.get_function_calls():
            if call.name =='update_conversation_name':
                continue
            msg = {
                "response_type": "tool_call",
                "content": {
                    "message": None,
                    "tool_name": call.name,
                    "tool_args": call.args,
                    "tool_response": None
                }
            }
            dbsession.add(Message(
                conversation_id=session_id,
                user_id=user_id,
                message_content=str(msg['content']),
                message_type="ai",
                send_time=datetime.utcnow()
            ))
            dbsession.commit()

            await websocket.send_text(json.dumps(msg))

        for fn_response in event.get_function_responses():
            if fn_response.name == 'update_conversation_name':
                dbsession.exec(update(Conversation)
                .where(Conversation.conversation_id == session_id)
                .values(conversation_name=fn_response.response['updated_name']))
                continue
            msg = {
                "response_type": "tool_response",
                "content": {
                    "message": None,
                    "tool_name": fn_response.name,
                    "tool_args": None,
                    "tool_response": fn_response.response
                }
            }
            dbsession.add(Message(
                conversation_id=session_id,
                user_id=user_id,
                message_content=str(msg['content']),
                message_type="ai",
                send_time=datetime.utcnow()
            ))
            dbsession.commit()
            await websocket.send_text(json.dumps(msg))

    message_dict = {
        "conversation_id": session_id,
        "user_id": user_id,
        "message_content": response['content']['message'],
        "send_time": datetime.utcnow(),
        'message_type': 'ai'
    }

    message = Message.model_validate(message_dict)
    dbsession.add(message)
    dbsession.commit()
    dbsession.refresh(message)
    dbsession.close()

    await websocket.send_text(json.dumps(response))
   
    