from abc import ABC, abstractmethod

from . import AuthInterface
from . import RawPluginInterface
from . import TaskInterface

class APIInterface(ABC):
    _auth: AuthInterface

    @abstractmethod
    def __init__(self, auth: AuthInterface) -> None:
        pass # pragma: no coverage

    def getAgent(self) -> None:
        pass # pragma: no coverage

    @abstractmethod
    def getPlugin(self, id: str) -> RawPluginInterface:
        pass # pragma: no coverage

    @abstractmethod
    def getTasks(self) -> [TaskInterface]:
        pass # pragma: no coverage

    @abstractmethod
    def putTaskResult(self, id: str, result: any) -> bool:
        pass # pragma: no coverage

    @abstractmethod
    def makeRequest(self, request, data) -> any:
        pass # pragma: no coverage