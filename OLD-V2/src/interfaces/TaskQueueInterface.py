from abc import ABC, abstractmethod

from . import TaskInterface
from . import TaskExecutorInterface

class TaskQueueInterface(ABC):
    _task_executor: TaskExecutorInterface

    @abstractmethod
    def __init__(self, task_executor: TaskExecutorInterface) -> None:
        pass # pragma: no cover

    @abstractmethod
    def addTask(self, task: TaskInterface) -> None:
        pass # pragma: no cover

    @abstractmethod
    def isTaskQueued(self, task: TaskInterface) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def start(self) -> None:
        pass # pragma: no cover

    @abstractmethod
    def stop(self) -> None:
        pass # pragma: no cover

    @abstractmethod
    def length(self) -> int:
        pass # pragma: no cover