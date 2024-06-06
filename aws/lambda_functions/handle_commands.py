import boto3
import json

from common.database import *
from common.message import *
from common.util import merge_responses

def lambda_handler(event, context):

    def get_commands(event_body: dict) -> list:
        contains_entities = "entities" in event_body["message"]

        if not contains_entities:
            return []
        
        commands = [event_body["message"]["text"][entity["offset"]+1:entity["offset"]+entity["length"]] \
                    for entity in event_body["message"]["entities"] if entity["type"] == "bot_command"]
        return commands

    def handle_command(command: str) -> dict:
        # Initialise status code and response
        status_code = 200
        response = None

        # Perform operations as per command and determine reply message
        match command:

            case "start":
                message = dialogues["start_success"]

                # Check if user has subscribed to notifications
                response = get_item(
                    dynamodb_client,
                    TableName = "Subscribers",
                    Key = {"chat_id": {"S": chat_id}}
                )
                response_status_code = response["status_code"]

                # Include prompt for subscribing / unsubscribing based on subscription status
                if response_status_code == 200:
                    is_subscriber = "Item" in response["body"]
                    if is_subscriber:
                        message += f"\n\n{dialogues['unsubscribe_prompt']}"
                    else:
                        message += f"\n\n{dialogues['subscribe_prompt']}"
                
                else:
                    message = response["text"]
                    status_code = response_status_code

            case "subscribe":
                response = put_item(
                    dynamodb_client, 
                    TableName = "Subscribers",
                    Item = {"chat_id": {"S": chat_id}}
                )
                response_status_code = response["status_code"]

                if response_status_code == 200:
                    message = dialogues["subscribe_success"]
                else:
                    message = response["text"]
                    status_code = response_status_code
            
            case "unsubscribe":
                response = delete_item(
                    dynamodb_client, 
                    TableName = "Subscribers",
                    Key = {"chat_id": {"S": chat_id}}
                )
                response_status_code = response["status_code"]

                if response_status_code == 200:
                    message = dialogues["unsubscribe_success"]
                else:
                    message = response["text"]
                    status_code = response_status_code

            case _:
                message = dialogues["fallback"]
        
        # Reply user
        new_response = send_message(TELEGRAM_BOT_TOKEN, chat_id, message, status_code)

        if response:
            response = merge_responses(response, new_response)
        else:
            response = new_response

        return {"status_code": response["status_code"], "text": response["text"]}

    ########################
    # Initialise resources #
    ########################

    # boto3 clients
    ssm_client = boto3.client("ssm")
    dynamodb_client = boto3.client("dynamodb")

    # assets
    with open("assets/dialogues.json", "r") as file:
        dialogues = json.load(file)
    
    # parameters
    TELEGRAM_BOT_TOKEN = ssm_client.get_parameter(Name="TELEGRAM_BOT_TOKEN")["Parameter"]["Value"]

    # session details
    event_body = json.loads(event["body"])
    chat_id = str(event_body["message"]["chat"]["id"])

    ##################
    # Handle command #
    ##################

    commands = get_commands(event_body)

    match len(commands):
        case 0:
            response = send_message(TELEGRAM_BOT_TOKEN, chat_id, "Please specify a command.")
        case 1:
            response = handle_command(commands[0])
        case _:
            response = send_message(TELEGRAM_BOT_TOKEN, chat_id, "Please specify one command at a time.")

    ###################
    # Return response #
    ###################

    return {
        'status_code': response["status_code"],
        'text': "Successfully handled command!" if response["status_code"] == 200 else response["text"]
    }