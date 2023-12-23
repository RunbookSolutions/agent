from modules.interfaces import AgentInterface, APIInterface, PluginManagerInterface, TaskQueueInterface, TaskSchedulerInterface

class Agent(AgentInterface):
    def __init__(self, api: APIInterface, plugin_manager: PluginManagerInterface, task_queue: TaskQueueInterface, task_scheduler: TaskSchedulerInterface) -> None:
        self._api = api
        self._plugin_manager = plugin_manager
        self._task_queue = task_queue
        self._task_scheduler = task_scheduler

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass