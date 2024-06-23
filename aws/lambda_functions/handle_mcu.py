import base64
import json
from datetime import datetime
import pytz

from common.database import *
from common.message import *
from common.util import *

def lambda_handler(event, context):

    #################
    # Get resources #
    #################

    # subscribers
    response = scan("Subscribers")
    subscribers = response["body"]

    # sensor readings
    mcu_data = json.loads(base64.b64decode(event["body"]).decode("utf-8"))

    # current time
    mcu_data["time"] = datetime.now(pytz.timezone("Asia/Singapore")).strftime("%Y%m%d%H%M%S")

    #########################
    # Store sensor readings #
    #########################

    response = put_item(
        TableName = "SensorReadings",
        Item = {k: {"N": v} for k, v in mcu_data.items()}
    )

    ####################################
    # Broadcast message (if necessary) #
    ####################################

    for subscriber in subscribers:

        if float(mcu_data["balcony_humidity"]) > 85:
            new_response = send_message(subscriber, ["rainfall_warning"], response)
            response = merge_responses(response, new_response)

    ###################
    # Return response #
    ###################

    return {
        'status_code': response["status_code"],
        'text': "Successfully handled sensor reading!" if response["status_code"] == 200 else response["text"]
    }