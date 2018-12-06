from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail,Message

from xorder import app

ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

mail = Mail(app)

def send_email(address, subject, body):
	msg = Message(recipients=[address])
	msg.html = body
	msg.subject = subject
	mail.send(msg)