from abc import ABC, abstractmethod

class TaskInterface(ABC):
    id: str
    cron: str
    command: str
    arguments: str

    @abstractmethod
    def __init__(self, id: str, cron: str, command: str, arguments: str) -> None:
        pass # pragma: no coverage 