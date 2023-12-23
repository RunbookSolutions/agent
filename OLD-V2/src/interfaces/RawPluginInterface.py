from abc import ABC, abstractmethod

class RawPluginInterface(ABC):
    id: str
    name: str
    version: str
    description: str
    draft: bool
    script: str
    hash: str
    commands: []

    @abstractmethod
    def __init__(self) -> None:
        pass  # pragma: no coverage

    @abstractmethod
    def save(self, path: str) -> None:
        pass # pragma: no coverage

    @abstractmethod
    def verify() -> bool:
        pass # pragma: no coverage