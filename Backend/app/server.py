import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .authentication import authentication
from .router import users, websocket


APP_NAME = 'gmail_agent'


app  = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}




# session_service = InMemorySessionService()
#
#
# async def create_session():
#     return await session_service.create_session(app_name=APP_NAME, user_id='samarth101', session_id='abcd101')
#
# runner = Runner(app_name=APP_NAME,
#                 session_service=session_service,
#                 agent=root_agent)


# @app.websocket('/app/{conversation_id}')
# async def message(websocket: WebSocket,conversation_id):
#     await create_session()
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await call_agent_async(prompt=data,
#                                runner=runner,
#                                USER_ID='samarth101',
#                                SESSION_ID=conversation_id,
#                                websocket=websocket)
#
# async def call_agent_async(prompt:str,runner,USER_ID,SESSION_ID,websocket: WebSocket):
#     print(f"\n>>> User Query: {prompt}")
#
#     # Prepare the user's message in ADK format
#     content = types.Content(role='user', parts=[types.Part(text=prompt)])
#
#     final_response_text = "Agent did not produce a final response."  # Default
#     async for event in runner.run_async(user_id=USER_ID,session_id=SESSION_ID, new_message=content):
#             if event.is_final_response():
#                 if event.content and event.content.parts:
#                     # Assuming text response in the first part
#                     final_response_text = event.content.parts[0].text
#                 elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
#                     final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
#                 # Add more checks here if needed (e.g., specific error codes)
#                 break
#             calls = event.get_function_calls()
#             if calls:
#                 for call in calls:
#                     tool_name = call.name
#                     arguments = call.args
#                     print(f"  Tool: {tool_name}, Args: {arguments}")
#                     await websocket.send_text(f"  Tool: {tool_name}, Args: {arguments}")
#             responses = event.get_function_responses()
#             if responses:
#                 for response in responses:
#                     tool_name = response.name
#                     result_dict = response.response
#                     print(f"  Tool Result: {tool_name} -> {result_dict}")
#                     await websocket.send_text(f"  Tool Result: {tool_name} -> {result_dict}")
#     print(f'final response text = {final_response_text}')
#     await websocket.send_text(f'final response text = {final_response_text}')



