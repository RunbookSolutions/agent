#!/bin/python

####
# Imports and Class Definition
####

from modules.interfaces import TaskExecutorInterface, PluginManagerInterface, TaskInterface
from modules import Agent, API, Auth, PluginManager, TaskQueue, TaskScheduler
class TaskExecutor(TaskExecutorInterface):
    _plugin_manager: PluginManagerInterface

    def __init__(self, plugin_manager: PluginManagerInterface):
        self._plugin_manager = plugin_manager

    def execute(self, task: TaskInterface) -> None:
        if self._plugin_manager.commandIsLoaded(task.command):
            self._plugin_manager.runCommand(task.command, task.arguments)

####
# Define Core Components
####

api = API(
    auth=Auth(enabled=False)
)
pluginManager = PluginManager()
taskExecutor = TaskExecutor(
    plugin_manager=pluginManager
)
taskQueue = TaskQueue(task_executor=taskExecutor)
taskScheduler = TaskScheduler(task_queue=taskQueue)

####
# Define Our Agent
####

agent = Agent(
    api=api,
    plugin_manager=pluginManager,
    task_queue=taskQueue,
    task_scheduler=taskScheduler
)

# Start Our Agent
agent.start()
