from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS setup (allow frontend to call)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend URL here in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sender_email = "gunner382269@gmail.com"
receiver_email = "sudhanshu.sharma.work.22@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = "465"
smtp_username = "gunner382269@gmail.com"
smtp_password = "ohqv sspq dnxg maqs"


@app.get("/")
def read_root():
    return {"message": "EMAIL SENDER"}

@app.post("/submit")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    subject = f"New Contact Form Submission from {name}"
    body = f"""
    Name: {name}
    Email: {email}
    
    Message:
    {message}
    """

    send_email(subject, body)
    return {"message": "Form submitted successfully"}

def send_email(subject: str, body: str):

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("✅ Email sent")
    except Exception as e:
        print("❌ Email failed to send:", e)
