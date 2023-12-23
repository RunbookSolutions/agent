from abc import ABC, abstractmethod

from . import APIInterface
from . import PluginManagerInterface
from . import TaskQueueInterface
from . import TaskSchedulerInterface



class AgentInterface(ABC):
    _api: APIInterface
    _plugin_manager: PluginManagerInterface
    _task_queue: TaskQueueInterface
    _task_scheduler: TaskSchedulerInterface

    @abstractmethod
    def __init__(self, api: APIInterface, plugin_manager: PluginManagerInterface, task_queue: TaskQueueInterface, task_scheduler: TaskSchedulerInterface) -> None:
        pass # pragma: no coverage

    @abstractmethod
    def start(self) -> None:
        pass # pragma: no coverage 

    @abstractmethod
    def stop(self) -> None:
        pass # pragma: no coverage 