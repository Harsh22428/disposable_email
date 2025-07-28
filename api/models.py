#Validation models for email data using Pydantic
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime,timezone

class Attachment(BaseModel):
    filename: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    data: Optional[str] = None

class EmailModel(BaseModel):
    inbox: str = Field(..., description="Inbox name (user part of the email address)")
    from_address: EmailStr = Field(..., description="Sender's email address")
    to_address: EmailStr = Field(..., description="Recipient's email address")
    subject: Optional[str] = Field(None, description="Email subject")
    body: Optional[str] = Field(None, description="Main body of the email (plain or HTML)")
    date: datetime = Field(default_factory=datetime.now(timezone.utc), description="Received date/time")
    attachments: Optional[List[Attachment]] = Field(default_factory=list, description="List of attachments")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="Other email headers")
    id: Optional[str] = Field(None, alias="_id", description="MongoDB document ID")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
