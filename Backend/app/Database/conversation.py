from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel



class ConversationBase(SQLModel):
    conversation_id: UUID = Field(default_factory=uuid4,primary_key=True)

class Conversation(ConversationBase,table = True):
    __tablename__ = 'conversations'

    conversation_name: str = Field(nullable=False, max_length=255)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID = Field(default = None, foreign_key='Users.user_id')

class ConversationPublic(ConversationBase):
    conversation_name: str = Field(nullable=False, max_length=255)

