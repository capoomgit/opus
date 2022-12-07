import json
CREDENTIALS_PATH = "P:/pipeline/standalone_dev/libs/credentials.json"
def get_credentials() -> dict:
    """ Gets the credentials from the library and"""

    with open(CREDENTIALS_PATH, "r") as f:
        credentials = json.load(f)
    return credentials
