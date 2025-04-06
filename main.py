from fastapi import FastAPI, Form
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

## ({phone, message, name, adress, carnane}) - >  message 


@app.get("/")
def read_root():
    return {"message": "EMAIL SENDER"}


@app.post("/submit")
def submit_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

    send_email(subject, body)
    return {"message": "Form submitted successfully"}

def send_email(subject, body):
    sender_email = "..."
    receiver_email = "..."
    password = "..."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
