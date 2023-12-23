from concurrent.futures import ThreadPoolExecutor
from threading import Event
from queue import Queue, Empty

from modules.interfaces import TaskInterface, TaskExecutorInterface, TaskQueueInterface

class TaskQueue(TaskQueueInterface):
    _task_executor: TaskExecutorInterface
    _queue: Queue
    _tasks: {str: TaskInterface}

    def __init__(self, task_executor: TaskExecutorInterface) -> None:
        self._task_executor = task_executor
        self._stop_event = Event()
        self._queue = Queue()
        self._tasks = []
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._tasks = {}

    def addTask(self, task: TaskInterface) -> None:
        if not self.isTaskQueued(task):
            self._tasks[task.id] = task
            self._queue.put(task.id)

    def isTaskQueued(self, task: TaskInterface) -> bool:
        return task.id in self._tasks

    def start(self) -> None:
        self._threads = [self._executor.submit(self._worker) for _ in range(4)]

    def stop(self) -> None:
        self._stop_event.set()

        for thread in self._threads:
            thread.cancel()

        for thread in self._threads:
            thread.result(timeout=1)

    def length(self) -> int:
        return len(self._tasks)
    
    def _worker(self) -> None:
        while not self._stop_event.is_set():
            try:
                task_id = self._queue.get(timeout=1)
                task = self._tasks.pop(task_id, None)
                if task:
                    self._task_executor.execute(task)
            except Empty:
                pass
        
        
