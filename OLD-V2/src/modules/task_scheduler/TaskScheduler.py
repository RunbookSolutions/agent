from croniter import croniter
from dateutil.relativedelta import relativedelta
from threading import Event, Thread
from time import sleep
from datetime import datetime
from modules.interfaces import TaskSchedulerInterface, TaskQueueInterface, TaskInterface

class TaskScheduler(TaskSchedulerInterface):
    _tasks: [TaskInterface]
    _stop_event: Event

    def __init__(self, task_queue: TaskQueueInterface) -> None:
        self._task_queue = task_queue
        self._tasks = []
        self._thread = None
        self._stop_event = Event()

    def addTask(self, task: TaskInterface) -> None:
        if self.isTaskScheduled(task):
            self.updateTask(task=task)
        else:
            self._tasks.append(task)
    
    def removeTask(self, id: str) -> None:
        self._tasks = [task for task in self._tasks if task.id != id]

    def isTaskScheduled(self, task: TaskInterface) -> bool:
        return task.id in [_task.id for _task in self._tasks]
    
    def updateTask(self, task: TaskInterface) -> None:
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task.id:
                # Replace the existing task with the new one
                self._tasks[i] = task
                break

    def start(self) -> None:
        if not self._thread or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = Thread(target=self._worker)
            self._thread.start()

    def stop(self) -> None:
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()

    def shouldRun(self, cron_expresion: str) -> bool:
        cron = croniter(cron_expresion, datetime.now())
        td, ms1 = cron.get_current(datetime), relativedelta(microseconds=1)
        if not td.microsecond:
            td = td + ms1
        cron.set_current(td, force=True)
        tdp, tdt = cron.get_current(), cron.get_prev()
        precision_in_seconds = 1
        return (max(tdp, tdt) - min(tdp, tdt)) < precision_in_seconds

    def length(self) -> int:
        return len(self._tasks)

    def _worker(self) -> None:
        while not self._stop_event.is_set():
            for task in self._tasks:
                if self.shouldRun(task.cron):
                    self._task_queue.addTask(task)
            sleep(1)