from flask import Flask, render_template, flash, redirect, url_for, request
from config import Config
from flask_mail import Mail, Message
import pika
import json
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

def callback(ch, method, properties, body):
  url_map = json.loads(body)
  with app.app_context():
    html = render_template('activate.html', confirm_url=url_map["confirm_url"])
    subject = "Follow the link to confirm your email"
    mail.send(Message(subject, recipients=[url_map["email"]], html=html, sender=app.config['MAIL_USERNAME']))

conn_params = pika.ConnectionParameters(host='rabbitmq', port=5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue='rabbit-queue')
channel.basic_consume(queue='rabbit-queue', on_message_callback=callback, auto_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()
