# File agent/api.py
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import requests

class API:
    def __init__(self, api_url, agent):
        self.api_url = str(api_url)
        self.api_token = None
        self.agent = agent

    def authenticate(self):
        # Implement your authentication logic here, e.g., setting headers, tokens, etc.
        # You can use self.api_url and self.api_token for authentication
        pass

    def get_graphql_client(self):
        headers = {'Authorization': f'Bearer {self.api_token}'}
        transport = RequestsHTTPTransport(url=self.api_url, headers=headers, use_json=True)
        return Client(transport=transport)

    def send_query(self, query):
        client = self.get_graphql_client()
        response = client.execute(gql(query))
        return response
    
    async def poll(self):
        response = requests.get(f"{self.api_url}/poll")
        try:
            # Check if the response status code is 200 (OK) before parsing and printing the JSON
            if response.status_code == 200:
                response_json = response.json()  # Parse the response content as JSON
                # print(json.dumps(response_json, indent=2))  # Pretty-print the JSON
                for item in response_json:
                    self.agent.put_event(item)
            else:
                print(f"Error: {response.status_code}")
        except json.decoder.JSONDecodeError:
            pass

        return []