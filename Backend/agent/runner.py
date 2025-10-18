from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from .agent import root_agent
from Backend.Database.Users import User,UserPublic
from Backend.Database.conversation import Conversation
from Backend.Database.messages import Message
from Backend.Database.database import get_session
import json
from datetime import datetime


APP_NAME = "gmail_agent"

dbsession = next(get_session())

session_service = DatabaseSessionService(
    db_url='postgresql://samarth:samarth2410@localhost:5432/ai_db'
)
runner = Runner(app_name=APP_NAME,
                session_service=session_service,
                agent=root_agent)

async def create_session(user_id,conversation_id):
    return await session_service.create_session(app_name=APP_NAME,
                                                user_id=str(user_id),
                                                session_id=str(conversation_id))

async def call_agent_async(prompt: str,runner, user_id, session_id, websocket):
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(user_id=str(user_id), session_id=str(session_id), new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

        for call in event.get_function_calls():
            await websocket.send_text(f"Tool: {call.name}, Args: {call.args}")

        for response in event.get_function_responses():
            await websocket.send_text(f"Tool Result: {response.name} -> {response.response}")

    message_dict = {
        "conversation_id": session_id,
        "user_id": user_id,
        "message_content": final_response_text,
        "send_time": datetime.utcnow(),
        'message_type': 'ai'
    }

    message = Message.model_validate(message_dict)
    dbsession.add(message)
    dbsession.commit()
    dbsession.refresh(message)
    dbsession.close()

    await websocket.send_text(f"final response text = {final_response_text}")
