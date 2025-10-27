from google.adk import Agent
from dotenv import load_dotenv
import os
from agent.tools.tool import send_email,update_conversation_name
from .prompt import prompt


load_dotenv()


gmail_agent = Agent(
    name = 'gmail_service_agent',
    model = os.getenv('MODEL'),
    instruction = prompt,
    tools = [send_email,update_conversation_name]
)

root_agent = gmail_agent

