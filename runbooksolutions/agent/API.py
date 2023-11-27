from runbooksolutions.auth.Auth import Auth
from runbooksolutions.agent.Task import Task
import requests
import logging

class AgentDetails:
    id: str
    name: str
    team_id: str
    plugins = list
    def __init__(self, response: dict) -> None:
        response = response.get('data')
        self.id = response.get('id')
        self.name = response.get('name')
        self.team_id = response.get('team_id')
        if response.get('plugins') == None:
            self.plugins = []
        else:
            self.plugins = response.get('plugins')

class AgentTasks:
    tasks: [Task]

    def __init__(self, response: dict) -> None:
        self.tasks = []
        response = response.get('data')
        for task in response:
            self.tasks.append(Task(task))

    def getTasks(self):
        return self.tasks

class API:
    url: str = None
    auth: Auth = None

    def __init__(self, auth: Auth, url: str) -> None:
        self.auth = auth
        self.url = url + "/api"

    def getAgentDetails(self) -> AgentDetails:
        return AgentDetails(self.sendRequest('/agent', 'GET'))
    
    def getAgentTasks(self) -> AgentTasks:
        return AgentTasks(self.sendRequest('/agent/tasks', 'GET'))
    
    def sendTaskResult(self, task: Task, result: any):
        self.sendRequest(
            f'/agent/task/{task.id}',
            'POST',
            {'data':result}
        )

    def sendRequest(self, url, method, data=None):
        url = self.url + url
        headers = self.auth.getHeaders()  # Assuming Auth has a method to get authentication headers
        method = method.upper()

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
        if response.status_code != 200 and response.status_code != 201:
            raise Exception(f"Request failed with status code {response.status_code}. Response content: {response.text}")

        return response.json()  # Assuming the response is in JSON format