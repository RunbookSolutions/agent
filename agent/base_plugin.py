#File: /agent/base_plugin.py

from abc import ABC, abstractmethod

class BasePlugin(ABC):

    def __init__(self, options):
        self.options = options

    async def setup(self, agent):
        self.agent = agent

    @abstractmethod
    async def handle(self, event):
        pass

    @abstractmethod
    async def teardown(self):
        pass

    @abstractmethod
    # This method should be implemented by plugins to specify if they should handle the event.
    async def should_handle(self, event):
        return True