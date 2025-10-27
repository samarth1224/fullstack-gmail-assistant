import base64
import json
import os
from email.message import EmailMessage
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow 
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from google.adk.sessions import DatabaseSessionService
from google.adk.tools import ToolContext,FunctionTool

from app.Database.Users import User
from app.Database.database  import get_session
from sqlmodel import Session,select

load_dotenv()


GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID') # For token verification
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET') # For OAuth flow


def update_conversation_name(tool_context: ToolContext,updated_name: str):
    """update the conversation name.
        Args: 
            updated_name: The new name of the conversation. Must be short and precise and overview of the user conversation/session history.
        Returns: 
            Dict with operation result
    """
    tool_context.state['conv_name'] = updated_name
    return {'result':'success',
    'updated_name': updated_name}

def send_email(tool_context: ToolContext,to: str,
                     subject: str,
                     content: str,
                     ) -> Dict[str, Any]:
    """
    Send an email via Gmail.

    Args:
            to: Recipient email address
            subject: Email subject
            content: Email content/body
            from_email: Sender email (optional, uses authenticated user's email)

    Returns:
            Dict with operation result
    """
    try:
        user_id = tool_context._invocation_context.user_id
        dbsession = next(get_session())
        current_user = dbsession.exec(select(User).where(User.user_id == user_id)).first()
        creds = Credentials(
            token=current_user.access_token,
            refresh_token=current_user.refresh_token,
            token_uri= os.getenv('TOKEN_URI'),
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
        )
    except Exception as e:
        return {"success": False,'error_message':f'{e}.Please authorize'}

    if not creds or not creds.valid:
        return {"success": False, "error_message": "Cannot proceed without valid credentials."}

        # Validate inputs
    if not to or not subject or not content:
        return {
           "success": False,
            "message": "Missing required fields: to, subject, and content are required"
        }

    try:
        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)

        # Create email message
        message = EmailMessage()
        message.set_content(content)
        message["To"] = to
        message["From"] = current_user.emailid
        message["Subject"] = subject

        # Encode and send
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        result = service.users().messages().send(
            userId="me",
            body=create_message
        ).execute()

        return {
            "success": True,
            "message_id": result.get("id"),
            "message": f"Email sent successfully to {to}"
        }

    except HttpError as e:
        error_msg = f"Gmail API error: {str(e)}"
        if e.resp.status == 401:
            error_msg = "Authentication expired. Please re-authenticate."
        elif e.resp.status == 403:
            error_msg = "Insufficient permissions. Check Gmail API access."

        return {
            "success": False,
            "message": error_msg
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Unexpected error: {str(e)}"
        }
   


def get_mail_info(self):
    pass


def arrange_mails(self):
    pass


def delete_mails(self):
    pass


def create_drafts(self):
    pass

