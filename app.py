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

# In-memory "database" - replace with a proper database for production use.
user_first_time = {}

def send_sms(to_number, msg):
    twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)
    twilio_client.messages.create(
        to=to_number,
        from_=TWILIO_NUMBER,
        body=msg
    )

def gpt_answer(prompt):
    gpt_response = openai.Completion.create(
        engine="davinci-codex",
        prompt=(
            f"{prompt}\n\n"
            f"1. {prompt} - Simple Answer:\n"
            f"2. {prompt} - Include a link:\n"
        ),
        max_tokens=100,  # Adjust this to control the answer length
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = gpt_response.choices[0].text.strip()

    # Extract the Simple Answer and Answer with Link sections
    response_parts = response_text.split("1.")
    answer_simple = response_parts[1].split("2.")[0].strip()
    answer_with_link = response_parts[1].split("2.")[1].strip()

    if "LINK" in answer_with_link:
        return answer_with_link
    return answer_simple


@app.route("/sms", methods=["POST"])
def process_sms():
    sender_number = request.form["From"]
    message_body = request.form["Body"]

    response = MessagingResponse()

    if sender_number not in user_first_time:
        user_first_time[sender_number] = message_body
        send_sms(sender_number, "Terms of Service: [Link to ToS page] Please accept by replying 'Accept'.")

    elif message_body.lower() == 'accept':
        answer = gpt_answer(user_first_time[sender_number])
        send_sms(sender_number, f"Thank you for accepting the Terms of Service. Here's the answer to your question: {answer}")
    else:
        # Save the question before sending terms
        if sender_number in user_first_time:
            user_first_time[sender_number] = message_body
        
        answer = gpt_answer(message_body)
        send_sms(sender_number, answer)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)