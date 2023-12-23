from abc import ABC, abstractmethod

from . import TaskInterface

class TaskExecutorInterface(ABC):
    @abstractmethod
    def execute(self, task: TaskInterface) -> None:
        pass # pragma: no coverage