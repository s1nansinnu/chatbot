from pydantic import BaseModel
from typing import List, Optional

class chatRequest(BaseModel):
    SessionId: Optional[str]= None
    Message: str

class chatResponse(BaseModel):
    SessionId: str
    Response: str
    TokensUsed: int

class MessageHistory(BaseModel):
    role: str
    content: str

class sessionresponse(BaseModel):
    SessionId: str