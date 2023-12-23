from abc import ABC, abstractmethod

class AuthInterface(ABC):
    _enabled: bool
    _server_url: str

    @abstractmethod
    def __init__(self, enabled: bool) -> None:
        pass # pragma: no coverage

    @abstractmethod
    def getHeaders(self) -> {str, str}:
        pass # pragma: no coverage
