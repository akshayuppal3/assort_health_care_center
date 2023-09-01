import time
import uuid

def generate_custom_uuid():
    current_time = time.strftime("%Y%m%d-%H%M%S")
    unique_id = str(uuid.uuid4().fields[-1])[:4]
    username = "user"
    custom_uuid = f"{current_time}-{unique_id}-user"
    return custom_uuid

def send_client_message(client, receiver, message) -> bool:
    
    message_status = client.messages.create(from_="+18777994421", body=message, to=receiver)
    print("message body", message_status.body,"message arg", message, "to", message_status.to)

    if message_status.status != "sent" or message_status.error_code is not None:
        return False
    return True

def format_message(patient_details: dict, doctor_details: dict):
    # can later format it to be more cleaner
    return "Patient details: " + str(patient_details) + "\nDoctor details: " + str(doctor_details)
