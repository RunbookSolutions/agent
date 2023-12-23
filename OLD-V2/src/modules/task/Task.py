from modules.interfaces import TaskInterface

class Task(TaskInterface):
    id: str
    cron: str
    def __init__(self, id: str) -> None:
        self.id = id