#Handles User relation in database.
from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    username: str = Field(nullable=False, max_length=255)

class User(UserBase, table=True):
    __tablename__ = 'Users'

    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    emailid: str = Field(nullable=False)
    sub: str = Field(nullable=False, unique= True)

    access_token: str | None = Field(default=None)
    refresh_token: str | None = Field(default=None)
    scopes: str | None = Field(default= None)

class UserPublic(UserBase):
    user_id: UUID

class UserCreate(UserBase):
    emailid: str
    sub: str

class UserUpdate(UserBase):
    username: str | None = None
    emailid: str | None = None




