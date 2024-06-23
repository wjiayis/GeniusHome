import json

from common.database import *
from common.message import *
from common.util import *

def lambda_handler(event, context):

    def get_commands(event_body: dict) -> list:
        contains_entities = "entities" in event_body["message"]

        if not contains_entities:
            return []
        
        commands = [event_body["message"]["text"][entity["offset"]+1:entity["offset"]+entity["length"]] \
                    for entity in event_body["message"]["entities"] if entity["type"] == "bot_command"]
        return commands

    def handle_command(command: str) -> dict:
        # Initialise response
        response = init_response()

        # Perform operations as per command and determine reply message
        match command:

            case "start":
                message_keys = ["start_success"]

                # Check if user has subscribed to notifications
                new_response = get_item(
                    TableName = "Subscribers",
                    Key = {"chat_id": {"S": chat_id}}
                )
                response = merge_responses(response, new_response)

                # Include prompt for subscribing / unsubscribing based on subscription status
                if new_response["status_code"] == 200:
                    is_subscriber = "Item" in new_response["body"]
                    if is_subscriber:
                        message_keys.append("unsubscribe_prompt")
                    else:
                        message_keys.append("subscribe_prompt")


            case "subscribe":
                message_keys = ["subscribe_success"]

                new_response = put_item(
                    TableName = "Subscribers",
                    Item = {"chat_id": {"S": chat_id}}
                )
                response = merge_responses(response, new_response)
            
            case "unsubscribe":
                message_keys = ["unsubscribe_success"]

                new_response = delete_item(
                    TableName = "Subscribers",
                    Key = {"chat_id": {"S": chat_id}}
                )
                response = merge_responses(response, new_response)

            case "dev":
                message_keys = ["developer_success"]

                response = put_item(
                    TableName = "Developers",
                    Item = {"chat_id": {"S": chat_id}}
                )
                response = merge_responses(response, new_response)

            case _:
                message_keys = ["command_fallback"]
        
        # Reply user
        new_response = send_message(chat_id, message_keys, response)
        response = merge_responses(response, new_response)

        return {"status_code": response["status_code"], "text": response["text"]}

    #################
    # Get resources #
    #################
    event_body = json.loads(event["body"])
    chat_id = str(event_body["message"]["chat"]["id"])

    ##################
    # Handle command #
    ##################

    commands = get_commands(event_body)

    match len(commands):
        case 0:
            response = send_message(chat_id, "Please specify a command.")
        case 1:
            response = handle_command(commands[0])
        case _:
            response = send_message(chat_id, "Please specify one command at a time.")

    ###################
    # Return response #
    ###################

    return {
        'status_code': response["status_code"],
        'text': "Successfully handled command!" if response["status_code"] == 200 else response["text"]
    }