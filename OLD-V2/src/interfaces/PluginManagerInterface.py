from abc import ABC, abstractmethod

from . import PluginInterface

class PluginManagerInterface(ABC):
    @abstractmethod
    def savePlugin(self, plugin: PluginInterface) -> bool:
        pass # pragma: no coverage 
    
    @abstractmethod
    def removePlugin(self, id: str) -> bool:
        pass # pragma: no coverage 

    @abstractmethod
    def loadPlugin(self, id: str) -> bool:
        pass # pragma: no coverage 

    @abstractmethod
    def unloadPlugin(self, id: str) -> bool:
        pass # pragma: no coverage 

    @abstractmethod
    def commandIsLoaded(self, command: str) -> bool:
        pass # pragma: no coverage 

    @abstractmethod
    def runCommand(self, command: str, arguments: dict):
        pass # pragma: no coverage 