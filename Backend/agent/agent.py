from google.adk import Agent
from dotenv import load_dotenv
import os
from agent.tools.tool import GmailTool
from .prompt import prompt

load_dotenv()

app_crednitals = os.getenv('CREDENTIALS')
gmail = GmailTool(app_credentials_path=app_crednitals)

authentication_status = gmail.get_auth_status
authenticate_user = gmail.authenticate
send_email = gmail.send_email

gmail_agent = Agent(
    name = 'gmail_service_agent',
    model = os.getenv('MODEL'),
    instruction = prompt,
    tools = [send_email,authenticate_user,authentication_status]
)

root_agent = gmail_agent

#
#
# APP_NAME = 'gmail_agent'
# USER_ID = 'SN1'
# SESSION_ID = 'abcd101'
#
# session_service = InMemorySessionService()
# async def create_session():
#     return await session_service.create_session(app_name=APP_NAME,user_id=USER_ID,session_id=SESSION_ID)
#
#
#
# runner = Runner(
#     app_name=APP_NAME,
#     agent=gmail_agent,
#     session_service=session_service
# )
#
#
#
#
# async def call_agent_async(prompt:str,runner,USER_ID,SESSION_ID):
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
#                     arguments = call.args  # This is usually a dictionary
#                     print(f"  Tool: {tool_name}, Args: {arguments}")
#
#             responses = event.get_function_responses()
#             if responses:
#                 for response in responses:
#                     tool_name = response.name
#                     result_dict = response.response  # The dictionary returned by the tool
#                     print(f"  Tool Result: {tool_name} -> {result_dict}")
#
#     print(f'final response text = {final_response_text}')
#
# async def run_conversation():
#     await create_session()
#     await call_agent_async(prompt='hello what are things you can help me with?',runner=runner,USER_ID=USER_ID,SESSION_ID=SESSION_ID)
#     await call_agent_async(prompt='okay can you send a morning greeting mail to samarthnimade@gmail.com?Choose content and subject and header everything yourself',runner=runner,USER_ID=USER_ID,SESSION_ID=SESSION_ID)
#     await call_agent_async(prompt='yes proceed with authenticaion',
#                            runner=runner, USER_ID=USER_ID, SESSION_ID=SESSION_ID)
# if __name__ == "__main__":
#         asyncio.run(run_conversation())


