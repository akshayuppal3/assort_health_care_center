import uuid

from flask import Blueprint, current_app, Flask, request
import requests as python_requests
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.rest import Client

from app.utils.util import format_message, generate_custom_uuid, send_client_message
from app.utils.schedule_doctor import schedule_appointment

main_bp = Blueprint('main', __name__)
USER_ID = None
SENDER = None

@main_bp.route("/")
def hello():
    return "Hello World!"


@main_bp.route("/welcome", methods=['GET', 'POST'])
def welcome():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    response = VoiceResponse()
    
    global SENDER
    SENDER = request.values.get('From')    

    # You can now use caller_number to identify the caller and customize your response
    print(f"Received call from {SENDER}")

    global USER_ID
    USER_ID = generate_custom_uuid()

    response.say('Hi, Welcome to Assort. How can I help you?', voice=current_app.config['VOICE_PROFILE'])
    response.redirect(f"/voice_input", method="GET")    

    return str(response)

@main_bp.route("/voice_input", methods=['GET', 'POST'])
def ask_user(): 
    """Utilize twilio speech to text transcriber"""
    # Start our TwiML response
    response = VoiceResponse()
    # Process gathered input    
    gather = Gather(input='speech', speech_model='automatic', action="/nlu_agent")    
    
    response.append(gather)

    return str(response)

@main_bp.route("/nlu_agent", methods=['POST', 'GET'])
def get_nlu_agent_info():
    """Pass transcription to nlu agent and then continue the call flow"""
    transcribed_text = request.form.get('SpeechResult')
    print("Received Transcribed Text:", transcribed_text)

    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
    twilio_client = Client(account_sid, auth_token)                      
    
    twilio_response = VoiceResponse()
    global USER_ID
    rasa_response = python_requests.post(current_app.config['RASA_NLU_ENDPOINT'], json={"sender": USER_ID, "message": transcribed_text})
    rasa_response_json = rasa_response.json()
    print("rasa json", rasa_response_json)

    if is_success_message(rasa_response_json):
        send_message(twilio_client, rasa_response_json)
        return str(twilio_response.say(f"thank you, you will receive a message shortly", voice=current_app.config['VOICE_PROFILE']))

    if rasa_response_json == []:
        # ask again 
        text = "Sorry, we couldn't understand your response."
        twilio_response.say(text, voice=current_app.config['VOICE_PROFILE'])        
        twilio_response.redirect(f"/voice_input", method="GET")
    else:        
        rasa_response_text = rasa_response_json[0].get("text")
        twilio_response.say(rasa_response_text, voice=current_app.config['VOICE_PROFILE'])
        # ask the next question
        twilio_response.redirect(f"/voice_input", method="GET")
    
    return str(twilio_response.say("Thank you sir"))


def is_success_message(rasa_response_json):
    status = any([entry.get("text") == "Success" for entry in rasa_response_json ])
    return status

def send_message(twilio_client, rasa_response_json):
    global SENDER
    for entry in rasa_response_json:
        if "custom" in entry:
            user_details = entry.get("custom")
            message = format_message(user_details, schedule_appointment())
            send_client_message(twilio_client, SENDER, (message))
