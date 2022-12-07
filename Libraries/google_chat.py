from json import dumps
from httplib2 import Http

LIBS_PATH = "P:/pipeline/standalone_dev/libs"

from get_credentials import get_credentials


def send_message(message):

    json_url = get_credentials()["google_webhook_url"]
    url = json_url
    bot_message = {
        # 'text': 'HEY <users/all> BEN `OPTIMUS` *PRIME*'
        'text': message
        }
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    # print(response)

# if __name__ == '__main__':
#     send_to_chats('https://www.youtube.com/watch?v=bn1YCClRF-g')