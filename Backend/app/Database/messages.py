from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Column, Field, SQLModel, TEXT



class MessageBase(SQLModel):
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)

class Message(MessageBase,table = True):
    __tablename__ = 'messages'
    message_id: UUID = Field(default_factory=uuid4, primary_key=True)

    conversation_id: UUID = Field(default = None, foreign_key='conversations.conversation_id')
    user_id: UUID = Field(default=None, foreign_key='Users.user_id')
    message_content: str = Field(default=None, sa_column=Column(TEXT))
    send_time: datetime = Field(default=None)
    message_type: str = Field(default=None)
class MessagePublic(MessageBase):
    message_content: str = Field(default=None, sa_column=Column(TEXT))
    message_type: str = Field(default=None)



