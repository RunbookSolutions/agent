from abc import ABC, abstractmethod

class AuthInterface(ABC):
    enabled: bool
    @abstractmethod
    def __init__(self, enabled: bool) -> None:
        pass  # pragma: no coverage

    def getHeaders(self) -> {str: str}:
        pass # pragma: no coverage