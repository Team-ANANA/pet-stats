import requests
import json
import logging

class petfinder_utils:

    def __init__(self, env) -> None:
        self.payload = env.get('petfinder_payload')
    def get_access_token(self):
        logging.info('Getting petfinder access token')
        
        url = "https://api.petfinder.com/v2/oauth2/token"

        payload=self.payload
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        access_token = json.loads(response.text).get('access_token')

        if response.status_code != 200 or access_token is None:
            logging.fatal("Error getting access code from Petfinder. Exiting.")
            exit()
        
        logging.info(f"Loaded petfinder access token: {access_token}")

        return access_token

    def get_petfinder_data(self, path, access_token, payload = {}):

        logging.debug(f"Getting petfinder data at {path}")
        url = f"https://api.petfinder.com{path}"

        headers = {
        "Authorization": f"Bearer {access_token}"
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200 or response.text is None:
            logging.fatal(f"Error getting data for: {path}. Exiting")
            exit()
        
        return json.loads(response.text)
