# agent/agent.py
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from agent.output import Output
from agent.api import API
import configparser
import os
import threading
from agent.runner import Runner
from queue import Queue

class Agent:
    def __init__(self):
        self.event_bus = Queue()
        self.plugins = []
        self.scheduler = AsyncIOScheduler()
        self.output = Output()

        self.running_jobs = set()

        config = configparser.ConfigParser()
        config.read('agent.ini')
        self.api = API(config.get('API', 'api_url'), self)
        if config.has_option('API', 'poll_interval'):
            self.add_periodic_task(int(config.get('API', 'poll_interval')), self.api.poll)
        else:
            self.add_periodic_task(30, self.api.poll)

    async def start(self):
        # Start the event loop
        await self.run()

    def put_event(self, event):
        self.output.debug(f"Adding Event: {event} to the bus")
        self.event_bus.put(event)

    async def add_plugin(self, plugin):
        await plugin.setup(self)
        self.plugins.append(plugin)

    async def add_plugin_by_name(self, plugin_info):
        plugin_name = plugin_info['name'].lower()
        try:
            plugin_module = f'plugins.{plugin_name}.plugin'
            plugin_class = getattr(__import__(plugin_module, fromlist=['Plugin']), 'Plugin')
            plugin_instance = plugin_class(plugin_info['options'])
            await self.add_plugin(plugin_instance)
            self.output.success(f"Plugin [{plugin_name}] Loaded!")
        except (ImportError, AttributeError):
            self.output.error(f"Could not add plugin: {plugin_name}")

    def add_periodic_task(self, interval, task_function):
        self.output.debug(f"Adding Task: {task_function} to run every {interval} seconds")
        self.scheduler.add_job(task_function, 'interval', seconds=interval)

    async def run(self):
        # Start the scheduler
        scheduler_thread = threading.Thread(target=self.start_scheduler)
        scheduler_thread.start()

        runner = Runner(self.event_bus, self)
        runner.start()
        while True:
            await asyncio.sleep(1)

    def start_scheduler(self):
        self.output.debug(f"Starting the Scheduler.")

        # Set up a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Start the scheduler in the new event loop
        self.scheduler._eventloop = loop
        self.scheduler.start()
        loop.run_forever()

    def handle_event(self, event):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.handle_event_coroutine(event))
        loop.close()

    async def handle_event_coroutine(self, event):
        for plugin in self.plugins:
            if await plugin.should_handle(event):
                plugin_folder = os.path.basename(os.path.dirname(plugin.__class__.__module__))
                self.output.debug(f"Running Plugin: {plugin_folder.lower()}")
                await plugin.handle(event)