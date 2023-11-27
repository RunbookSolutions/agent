from runbooksolutions.auth.Auth import Auth
from runbooksolutions.schedule.Schedule import Schedule
from runbooksolutions.queue.Queue import Queue
from runbooksolutions.agent.API import API
from runbooksolutions.agent.API import AgentDetails
from runbooksolutions.agent.PluginManager import PluginManager
import asyncio
import configparser
import logging

class Agent:
    auth: Auth = None
    schedule: Schedule = None
    queue: Queue = None
    api: API = None
    pluginManager: PluginManager = None

    agentDetails: AgentDetails = None

    def __init__(self, num_threads: int = 1) -> None:
        self.agentConfig = self.loadConfig()
        self.auth = Auth(
            url=self.agentConfig.get('server_url'), 
            client_id=self.agentConfig.get('client_id'),
            enabled=self.agentConfig.get('auth')
        )
        self.api = API(auth=self.auth, url=self.agentConfig.get('server_url'))
        self.pluginManager = PluginManager(self.api)
        self.queue = Queue(num_threads, self.pluginManager)
        self.schedule = Schedule(self.queue)

    def loadConfig(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
            return config['agent']
        except FileNotFoundError:
            logging.critical("config.ini file not found!")
            exit()
        except configparser.Error:
            logging.critical("Error reading config file!")
            exit()

    async def syncAgent(self):
        while True:
            self.agentDetails = self.api.getAgentDetails()
            self.pluginManager.syncPlugins(self.agentDetails.plugins)

            tasks = self.api.getAgentTasks().getTasks()
            for task in tasks:
                if task.shouldSchedule():
                    self.schedule.add_task(task=task, cron_expression=task.cron)
                else:
                    await self.queue.enqueue_task(task)

            # Sleep for 60 seconds
            await asyncio.sleep(60)

    async def start(self) -> None:
        agent_task = asyncio.create_task(self.syncAgent())
        queue_task = asyncio.create_task(self.queue.start())
        schedule_task = asyncio.create_task(self.schedule.start())

        try:
            # Other asynchronous tasks can be started here...

            logging.info("End of Start")

            # Wait for the background task to complete
            await agent_task
            await queue_task
            await schedule_task
        except asyncio.CancelledError:
            logging.info("Agent task canceled. Stopping gracefully.")
        finally:
            self.queue.stop()
        
    def stop(self) -> None:
        self.queue.stop()