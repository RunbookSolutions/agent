import threading
from modules.interfaces import TaskExecutorInterface, TaskInterface
from modules.task_queue import TaskQueue
import time

class MockTaskExecutor(TaskExecutorInterface):
    count: int = 0
    def execute(self, task: TaskInterface):
        print(task)
        self.count +=1

class MockTask(TaskInterface):
    def __init__(self, id: str):
        self.id = id

def test_queue_can_have_tasks_added():
    executor = MockTaskExecutor()
    queue = TaskQueue(task_executor=executor)
    task = MockTask(id="1")

    assert queue.length() == 0

    queue.addTask(task)

    assert queue.length() == 1

def test_queue_can_have_tasks_added_but_wont_add_twice():
    executor = MockTaskExecutor()
    queue = TaskQueue(task_executor=executor)
    task = MockTask(id="1")

    assert queue.length() == 0
    queue.addTask(task)
    assert queue.length() == 1
    queue.addTask(task)
    assert queue.length() == 1

def test_queue_has_4_thread_by_default():
    executor = MockTaskExecutor()
    queue = TaskQueue(task_executor=executor)

    expected_thread_count = threading.active_count() + 4
    queue.start()
    actual_thread_count = threading.active_count()

    assert actual_thread_count == expected_thread_count

    queue.stop()


def test_queue_executes_tasks_with_provided_task_executor():
    executor = MockTaskExecutor()
    queue = TaskQueue(task_executor=executor)
    queue.start()

    assert queue.length() == 0
    task = MockTask(id="1")
    queue.addTask(task)
    time.sleep(1)
    

    queue.stop()
    assert executor.count == 1
