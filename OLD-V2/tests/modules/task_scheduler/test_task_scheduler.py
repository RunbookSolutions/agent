# Scheduler will start a single thread for itself
# Scheduler will add a task that needs to run into the queue

from modules.interfaces import TaskExecutorInterface, TaskInterface, TaskQueueInterface
from modules import TaskScheduler

import threading
import time

class MockTaskExecutor(TaskExecutorInterface):
    count: int = 0
    def execute(self, task: TaskInterface):
        print(task)
        self.count +=1

class MockTask(TaskInterface):
    def __init__(self, id: str, cron: str = None):
        self.id = id
        self.cron = cron

class MockTaskQueue(TaskQueueInterface):
    _tasks: [TaskInterface]
    def __init__(self, task_executor: TaskExecutorInterface) -> None:
        self._tasks=[]
        self._task_executor = task_executor

    def addTask(self, task: TaskInterface) -> None:
        self._tasks.append(task)

    def isTaskQueued(self, task: TaskInterface) -> bool:
        return False

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def length(self) -> int:
        return len(self._tasks)
    

def test_scheduler_can_have_task_added():
    executor = MockTaskExecutor()
    queue = MockTaskQueue(executor)

    scheduler = TaskScheduler(queue)

    assert scheduler.length() == 0

    task = MockTask(id="1")

    scheduler.addTask(task)

    assert scheduler.length() == 1

def test_scheduler_will_not_add_same_task_twice_but_update():
    executor = MockTaskExecutor()
    queue = MockTaskQueue(executor)

    scheduler = TaskScheduler(queue)

    assert scheduler.length() == 0

    task = MockTask(id="1")

    scheduler.addTask(task)

    assert scheduler.length() == 1
    assert scheduler._tasks[0].cron == None

    task = MockTask(id="1", cron="* * * * *")
    scheduler.addTask(task)

    assert scheduler.length() == 1
    assert scheduler._tasks[0].cron == "* * * * *"

def test_scheduler_can_remove_tasks():
    executor = MockTaskExecutor()
    queue = MockTaskQueue(executor)

    scheduler = TaskScheduler(queue)

    assert scheduler.length() == 0

    task = MockTask(id="1")

    scheduler.addTask(task)

    assert scheduler.length() == 1
    
    scheduler.removeTask("1")

    assert scheduler.length() == 0

def test_scheduler_starts_thread_for_itself():
    executor = MockTaskExecutor()
    queue = MockTaskQueue(executor)

    scheduler = TaskScheduler(queue)

    task = MockTask(id="1", cron="* * * * * *")
    scheduler.addTask(task)

    expected_thread_count = threading.active_count() + 1
    scheduler.start()
    time.sleep(1)
    actual_thread_count = threading.active_count()

    assert actual_thread_count == expected_thread_count

    scheduler.stop()