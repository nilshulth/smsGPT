import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai

app = Flask(__name__)

# Load environment variables from credentials.env
load_dotenv(".env")

# Twilio configuration
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

# OpenAI Configuration
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def send_sms(to_number, msg):
    twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
    twilio_client.messages.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        body=msg
    )

def gpt_answer(prompt):
    # Initialize the messages list for the Chat API
    messages = [
#        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt + ". If you deem it helpful for the person reading the answer, please include 1-2 links in the answer"},
    ]

    # Use the Chat API to get the model's response
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )

    # Extract the answer from the model's response
    answer = gpt_response.choices[0].message.content.strip()

    return answer

@app.route("/sms", methods=["POST"])
def process_sms():
    sender_number = request.form["From"]
    message_body = request.form["Body"]
    Print("Received an SMS '" + message_body + "' from: " + sender_number)

    response = MessagingResponse()

    answer = gpt_answer(message_body)
    send_sms(sender_number, answer)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)