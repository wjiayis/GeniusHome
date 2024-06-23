from botocore.exceptions import ClientError
import json

def handle_boto_exceptions(func):
    '''
    Decorator to handle boto exceptions
    '''
    def wrapper(*args, **kwargs):
        try:
            body, status_code, text = func(*args, **kwargs)
        except ClientError as e:
            body = None
            status_code = 400
            text = json.dumps(e.response["Error"])
        return {"body": body, "status_code": status_code, "text": text}
    return wrapper

def merge_responses(curr_response: dict, new_response: dict) -> dict:
    '''
    Update status code based on new status code, returning 200 only if both are 200.
    Update text based on new text by concatenating them together.
    '''

    response_status_code = curr_response["status_code"]
    response_text = curr_response["text"]
    new_response_status_code = new_response["status_code"]
    new_response_text = new_response["text"]

    if new_response_status_code != 200:
        response_status_code = new_response_status_code
        response_text = "\n\n".join([response_text, new_response_text]) if len(response_text) else new_response_text
    return {"status_code": response_status_code, "text": response_text}

def init_response() -> dict:
    return {"status_code": 200, "text": ""}