from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserMe(BaseModel):
    id: UUID
    username: str
    is_admin: bool
    created_at: datetime
