from abc import ABC, abstractmethod

from . import APIInterface

class PluginInterface(ABC):
    _api: APIInterface

    @abstractmethod
    def __init__(self, api: APIInterface) -> None:
        pass  # pragma: no coverage

    @abstractmethod
    def verify(self, hash: str) -> bool:
        pass # pragma: no coverage