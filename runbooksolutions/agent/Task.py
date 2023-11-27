import json

class Task:
    id: str
    command: str
    arguments: dict
    cron: str
    def __init__(self, task: dict) -> None:
        self.id = task.get('id')
        self.command = task.get('command')
        self.arguments = task.get('arguments')
        self.cron = task.get('cron')

    def shouldSchedule(self):
        return self.cron != None
    
    def getArguments(self):
        return json.loads(self.arguments)