import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"  # Replace with your email
SENDER_PASSWORD = "your_password"  # Replace with your email password
DOCTOR_EMAIL = "doctor@example.com"  # Replace with the doctor's email


def send_email_to_doctor(analysis):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = DOCTOR_EMAIL
        msg['Subject'] = "New Patient Analysis"

        body = f"A new patient analysis has been generated:\n\n{analysis}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(SENDER_EMAIL, DOCTOR_EMAIL, text)

        print("Analysis sent to doctor successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
