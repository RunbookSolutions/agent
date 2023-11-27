from runbooksolutions.auth.DeviceCode import DeviceCode
from runbooksolutions.auth.AccessToken  import AccessToken
import logging
import json
import requests
import time

class Auth:
    url: str
    client_id: str
    enabled: bool = True
    deviceCode: DeviceCode = None
    accessToken: AccessToken = None

    def __init__(self, url: str, client_id: str, enabled: bool = True) -> None:
        self.url = url
        self.client_id = client_id
        self.enabled = enabled

        logging.debug("Starting Authentication")
        if not self.enabled:
            return

        self.deviceCode = DeviceCode.load_from_store()
        self.accessToken = AccessToken.load_from_store()

        if self.accessToken is None:
            logging.debug("Access Token does not yet exist.")
            if self.deviceCode is None:
                logging.debug("Device code does not yet exist.")
                self.getDeviceCode()
            
            # We have a Device Code; so lets get our access tokens
            self.pollAuthorization()
        
        logging.debug("Finished Authentication")

    def getHeaders(self) -> dict:
        if not self.enabled:
            return {
                'Content-Type': 'application/json',
            }
        
        headers = {
            'Authorization': f'Bearer {self.accessToken.getAccessToken()}',
            'Content-Type': 'application/json',
        }
        return headers

    def getDeviceCode(self) -> None:
        logging.debug("Getting a device code.")
        myobj = {
            'client_id': self.client_id,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'scope': ''
        }
        url = f"{self.url}/oauth/device/code"

        try:
            response = requests.post(url, json=myobj)
            # Check the HTTP status code
            response.raise_for_status()

            self.deviceCode = DeviceCode(json.loads(response.text))

            logging.critical(f"{self.deviceCode.getVerificationURI()} CODE: {self.deviceCode.getUserCode()}")

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise Exception(f"Request failed: {e}")
        
    def pollAuthorization(self) -> None:
        logging.debug("Polling for user authorization...")

        while True:
            if self.deviceCode.isExpired():
                self.getDeviceCode()
            try:
                myobj = {
                    'client_id': self.client_id,
                    'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                    'device_code': self.deviceCode.getDeviceCode()
                }
                url = f"{self.url}/oauth/token"

                logging.debug(myobj)

                response = requests.post(url, json=myobj)
                logging.debug(f"Response Status Code: {response.status_code}")

                if response.status_code == 200:
                    logging.debug(type(response.text))
                    # Authorization successful, extract and store the access token
                    try:
                        # Try parsing the response as JSON
                        token_data = json.loads(response.text)
                        self.accessToken = AccessToken(token_data)
                        logging.debug(f"Access Token: {self.accessToken.getAccessToken()}")
                        break
                    except json.JSONDecodeError:
                        logging.error("Failed to parse response as JSON.")
                        raise Exception("Failed to parse response as JSON.")
                elif response.status_code == 400 and "authorization_pending" in response.json().get('error'):
                    # Authorization is still pending, wait and poll again
                    logging.debug(f"Authorization Pending")
                    time.sleep(5)
                elif response.status_code == 400 and "expired_token" in response.json().get('error'):
                    logging.error("Device code has expired.")
                    self.getDeviceCode()
                    # raise Exception("Device code has expired.")
                else:
                    logging.error(f"Failed to obtain access token: {response.text}")
                    raise Exception(f"Failed to obtain access token: {response.text}")

            except requests.RequestException as e:
                logging.error(f"Request failed: {e}")
                raise Exception(f"Request failed: {e}")