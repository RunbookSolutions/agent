from runbooksolutions.queue.Queue import Queue
from runbooksolutions.agent.Task import Task
from datetime import datetime
from croniter import croniter
import asyncio
import logging

class Schedule:
    queue: Queue = None

    def __init__(self, queue: Queue) -> None:
        self.queue = queue
        self.tasks = []

    def add_task(self, task: Task, cron_expression: str) -> None:
        task_id = task.id
        if not self._is_task_in_schedule(task_id):
            logging.debug("Added Task")
            self.tasks.append((task, cron_expression))
        else:
            logging.warning("Task already Scheduled")

    def remove_task(self, task_id: str) -> None:
        for i, (task, _) in enumerate(self.tasks):
            if task.id == task_id:
                logging.debug(f"Removing Task with ID {task_id} from schedule")
                del self.tasks[i]
                break

    async def start(self) -> None:
        logging.debug("Schedule Started")
        while True:
            for task, cron_expression in self.tasks:
                if self.shouldRun(cron_expression):
                    await self.queue.enqueue_task(task)
            await asyncio.sleep(1)

    def shouldRun(self, cron_expression):
        from dateutil.relativedelta import relativedelta
        cron = croniter(cron_expression, datetime.now())
        td, ms1 = cron.get_current(datetime), relativedelta(microseconds=1)
        if not td.microsecond:
            td = td + ms1
        cron.set_current(td, force=True)
        tdp, tdt = cron.get_current(), cron.get_prev()
        precision_in_seconds = 1
        return (max(tdp, tdt) - min(tdp, tdt)) < precision_in_seconds
    
    def _is_task_in_schedule(self, task_id: str) -> bool:
        for task, _ in self.tasks:
            if task.id == task_id:
                return True
        return False