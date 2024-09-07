import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "traviseni01@gmail.com"  # Replace with your email
SENDER_PASSWORD = "ptzb eiky atop qxej"  # Replace with your App Password or Gmail password
DOCTOR_EMAIL = "roselynmakia@gmail.com"  # Replace with the doctor's email


def send_email_to_doctor(analysis):
    try:
        # Set up the email message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = DOCTOR_EMAIL
        msg['Subject'] = "New Patient Analysis"

        # Attach the email body (analysis result)
        body = f"A new patient analysis has been generated:\n\n{analysis}"
        msg.attach(MIMEText(body, 'plain'))

        # Establish a secure connection with the Gmail SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login to your email account

        # Send the email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, DOCTOR_EMAIL, text)
        server.quit()

        print("Success: Email sent to doctor successfully!")

    except Exception as e:
        print(f"Error: Failed to send email: {str(e)}")


# Example of how to use the function
send_email_to_doctor("Patient analysis goes here.")
