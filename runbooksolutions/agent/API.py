from runbooksolutions.auth.Auth import Auth
import requests

class API:
    auth: Auth = None

    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    def sendRequest(self, url, method, data=None):
        headers = self.auth.getHeaders()  # Assuming Auth has a method to get authentication headers

        # Choose the appropriate requests method based on the provided 'method'
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Invalid HTTP method. Supported methods are GET, POST, PUT, and DELETE.")

        # You might want to handle response status codes and raise exceptions if needed
        if response.status_code != 200:
            raise Exception(f"Request failed with status code {response.status_code}. Response content: {response.text}")

        return response.json()  # Assuming the response is in JSON format