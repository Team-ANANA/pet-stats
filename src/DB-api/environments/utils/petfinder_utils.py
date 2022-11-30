import requests
import json

class petfinder_utils:

    def __init__(self, env) -> None:
        self.payload = env.get('petfinder_payload')
    def get_access_token(self):
        
        url = "https://api.petfinder.com/v2/oauth2/token"

        payload=self.payload
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text).get('access_token')

    def get_petfinder_data(self, path, access_token):
        url = f"https://api.petfinder.com{path}"

        payload={}
        headers = {
        "Authorization": f"Bearer {access_token}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)
