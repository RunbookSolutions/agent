from abc import ABC, abstractmethod

from . import TaskInterface
from . import TaskQueueInterface

class TaskSchedulerInterface(ABC):
    _task_queue: TaskQueueInterface

    @abstractmethod
    def __init__(self, task_queue: TaskQueueInterface) -> None:
        pass # pragma: no cover

    @abstractmethod
    def addTask(self, task: TaskInterface) -> None:
        pass # pragma: no cover

    @abstractmethod
    def removeTask(self, id: str) -> None:
        pass # pragma: no cover

    @abstractmethod
    def isTaskScheduled(self, task: TaskInterface) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def updateTask(self, task: TaskInterface) -> None:
        pass # pragma: no cover

    @abstractmethod
    def start(self) -> None:
        pass # pragma: no cover

    @abstractmethod
    def stop(self) -> None:
        pass # pragma: no cover

    @abstractmethod
    def shouldRun(self, cron_expresion: str) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def length(self) -> int:
        pass # pragma: no cover