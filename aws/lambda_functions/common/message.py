import boto3
import requests
import json
from typing import List

from common.util import handle_boto_exceptions

with open("assets/dialogues.json", "r") as file:
    dialogues = json.load(file)

ssm_client = boto3.client("ssm")
TELEGRAM_BOT_TOKEN = ssm_client.get_parameter(Name="TELEGRAM_BOT_TOKEN")["Parameter"]["Value"]

@handle_boto_exceptions
def send_message(chat_id: str, message_keys: List[str], response: dict):

    # Format message
    if response["status_code"] == 200:
        message = "\n\n".join(dialogues[key] for key in message_keys)
    else:
        message = f"Oh no! GeniusHome ran into an error:<pre><code>{response['text']}</code></pre>"
    
    # Send message
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html"
    response = requests.get(url)

    # Return response
    return None, response.status_code, response.text