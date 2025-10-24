from google.adk import Agent
from dotenv import load_dotenv
import os
from agent.tools.tool import send_email,get_auth_status
from .prompt import prompt


load_dotenv()


gmail_agent = Agent(
    name = 'gmail_service_agent',
    model = os.getenv('MODEL'),
    instruction = prompt,
    tools = [send_email,get_auth_status]
)

root_agent = gmail_agent

