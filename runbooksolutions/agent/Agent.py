from runbooksolutions.auth.Auth import Auth
from runbooksolutions.schedule.Schedule import Schedule
from runbooksolutions.queue.Queue import Queue
from runbooksolutions.agent.API import API
from runbooksolutions.agent.PluginManager import PluginManager
import asyncio
import logging

class Agent:
    auth: Auth = None
    schedule: Schedule = None
    queue: Queue = None
    api: API = None
    pluginManager: PluginManager = None

    def __init__(self, num_threads: int = 1) -> None:
        self.auth = Auth()
        self.api = API(self.auth)
        self.pluginManager = PluginManager(self.api)
        self.queue = Queue(num_threads, self.pluginManager)
        self.schedule = Schedule(self.queue)

        self.pluginManager.addPlugin("123456789")

    async def start(self) -> None:
        queue_task = asyncio.create_task(self.queue.start())
        schedule_task = asyncio.create_task(self.schedule.start())

        try:
            # Other asynchronous tasks can be started here...

            logging.info("End of Start")

            # Wait for the background task to complete
            await queue_task
            await schedule_task
        except asyncio.CancelledError:
            logging.info("Agent task canceled. Stopping gracefully.")
        finally:
            self.queue.stop()
        
    def stop(self) -> None:
        self.queue.stop()