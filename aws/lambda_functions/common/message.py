import requests

from common.util import handle_boto_exceptions

@handle_boto_exceptions
def send_message(token: str, chat_id: str, message: str, status_code: int = 200):
    # Format message
    if status_code != 200:
        message = f"Oh no! GeniusHome ran into an error:<pre><code>{message}</code></pre>"
    
    # Send message
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html"
    response = requests.get(url)

    # Return response
    return None, response.status_code, response.text