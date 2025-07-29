# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from .models import EmailModel
from .db import (
    get_emails_by_inbox,
    get_email_by_id,
    delete_email_by_id,
    get_database
)


app = FastAPI()

# Middleware to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.luxidevilott.com/","https://disposable-email-ui.vercel.app/"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (singleton) database instance
db = get_database()

@app.get("/")
def root():
    return {"status": "API is running!"}

@app.get("/inbox/{inbox_name}", response_model=List[EmailModel])
def emails_by_inbox(inbox_name: str):
    emails = get_emails_by_inbox(db, inbox_name)
    if not emails:
        raise HTTPException(status_code=404, detail="Inbox not found or no emails available")
    return emails

@app.get("/inbox/{inbox_name}/{email_id}", response_model=EmailModel)
def email_by_id(inbox_name: str, email_id: str):
    email = get_email_by_id(db, email_id)
    if not email:
        raise HTTPException(status_code=404, detail="No email found with the given ID")
    return email

@app.delete("/inbox/{inbox_name}/{email_id}")
def delete_email(inbox_name: str, email_id: str):
    success = delete_email_by_id(db, email_id)
    if not success:
        raise HTTPException(status_code=404, detail="Email not found")
    return {"detail": "Email deleted successfully"}
