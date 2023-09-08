import datetime
import imaplib
import os
import re
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values

envs = dotenv_values(".env")
# Access the environment variables
api_key = envs["API_KEY"]
db_url = envs["DB_URL"]
debug_mode = envs.get("DEBUG", False)


def send_report(receiver_email, reports, project_name):
    sender = "rfnshare@gmail.com"
    receiver = receiver_email

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Email Subject
    mail_title = f"Test Report of {project_name} " + str(current_time)

    print("*" * 80)
    mail_body = "Here is the report for the test run at " + str(current_time) + "\n\n"

    # Mail content, format, encoding
    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = Header(mail_title, "utf-8")

    message.attach(MIMEText(mail_body))

    for report in reports:  # add files to the message
        filename = os.path.basename(report)
        attachment = MIMEApplication(open(report, "rb").read(), _subtype="txt")
        attachment.add_header("Content-Disposition", "attachment", filename=filename)
        message.attach(attachment)

    print("Sending report...")
    print("*" * 80)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(envs["email_address"], envs["email_password"])
        server.sendmail(sender, receiver, message.as_string())
        print(f"Sent report successfully to {receiver_email} !!!")
        server.close()

    except Exception as e:
        print("Failed to send mail!!!, Error:", e)

    # function to read last email message


def get_otp_from_email(email_credentials=None):
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(email_credentials["email"], email_credentials["password"])
    mail.select("INBOX")
    result, data = mail.search(None, "ALL")
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    re_match = re.search(r"Your OTP is (\d{6})", str(raw_email))
    otp = re_match.groups()[0]
    return otp
