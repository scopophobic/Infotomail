from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import resend  
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Resend
resend.api_key = os.getenv("RESEND_API_KEY") # Add this key to Render's Env Vars
receiver_email = "sudhanshu.sharma.work.22@gmail.com"

@app.get("/")
def read_root():
    return {"message": "EMAIL SENDER ACTIVE"}

@app.post("/submit")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    subject = f"New Contact Form Submission from {name}"
    
    # Resend handles HTML beautifully
    body_html = f"""
    <h3>New Message from your Website</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong></p>
    <p style="background: #f4f4f4; padding: 10px; border-radius: 5px;">{message}</p>
    """

    success = send_email_via_resend(subject, body_html)
    
    if success:
        return {"message": "Form submitted successfully"}
    else:
        return {"message": "Failed to send email"}, 500

def send_email_via_resend(subject: str, html_content: str):
    try:
        # On the free tier, you MUST use this sender address
        params = {
            "from": "onboarding@resend.dev",
            "to": receiver_email,
            "subject": subject,
            "html": html_content,
        }
        
        resend.Emails.send(params)
        print("✅ Email sent via Resend API")
        return True
    except Exception as e:
        print(f"❌ Resend API Error: {e}")
        return False
