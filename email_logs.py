from jproperties import Properties
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from logger import logs

#============================================================================
# load properties file
props = Properties()
with open('strategy.properties', 'rb') as config_file:
    props.load(config_file)

sender_email = props.get("SENDER_EMAIL").data
sender_pass = props.get("SENDER_EMAIL_PASSWORD").data
receiver_email = props.get("RECEIVER_EMAIL").data
email_host = props.get("SENDER_EMAIL_HOST").data
email_port = int(props.get("SENDER_EMAIL_PORT").data)

#============================================================================
today_date = '{:%Y-%m-%d}'.format(datetime.now())
file_name = f'{today_date}.log'
file_path = f'logs\\{file_name}'

#============================================================================
def send_email(subject):
	message = MIMEMultipart()
	message['From'] = sender_email
	message['To'] = receiver_email
	message['Subject'] = subject

	with open(file_path, 'r') as file:
		file_text = file.read()
		message.attach(MIMEText(file_text, 'plain'))

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
