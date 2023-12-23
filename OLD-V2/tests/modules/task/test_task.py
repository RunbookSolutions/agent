from modules.task import Task

def test_task_has_id():
    task = Task(id="Test_ID")
    assert(task.id == "Test_ID")