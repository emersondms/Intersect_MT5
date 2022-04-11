import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from logger import logs

#============================================================================
sender_email = os.environ['SENDER_EMAIL']
sender_pass = os.environ['SENDER_PASSWORD']
receiver_email = os.environ['RECEIVER_EMAIL']
email_host = 'smtp.gmail.com'
email_port = 587

#============================================================================
today_date = '{:%Y-%m-%d}'.format(datetime.now())
file_name = f'{today_date}.log'
attach_file_path = f'logs\\{file_name}'

#============================================================================
def send_email(subject, body):
	message = MIMEMultipart()
	message['From'] = sender_email
	message['To'] = receiver_email
	message['Subject'] = subject
	message.attach(MIMEText(body, 'plain'))

	with open(attach_file_path, 'r') as file:
		attach_file = file.read()
		payload = MIMEBase('application', 'octate-stream')
		payload.set_payload(attach_file)
		encoders.encode_base64(payload) 
		payload.add_header('Content-Disposition', 'attachment', filename=file_name)
		message.attach(payload)

	try:
		session = smtplib.SMTP(email_host, email_port) 
		session.starttls() #enable security
		session.login(sender_email, sender_pass) 
		text = message.as_string()
		session.sendmail(sender_email, receiver_email, text)
		session.quit()
		logs.info("Email sent")
	except Exception as ex:
		logs.error(f"Send email failed: {ex}")
