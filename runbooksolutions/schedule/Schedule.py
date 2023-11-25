from runbooksolutions.queue.Queue import Queue
from datetime import datetime
from croniter import croniter
import asyncio
import logging

class Schedule:
    queue: Queue = None

    def __init__(self, queue: Queue) -> None:
        self.queue = queue
        self.tasks = []

    def add_task(self, task: dict, cron_expression: str) -> None:
        logging.debug("Added Task")
        self.tasks.append((task, cron_expression))

    # async def start(self) -> None:
    #     logging.debug("Schedule Started")
    #     while True:
    #         current_time = datetime(
    #                               datetime.now().year, 
    #                               datetime.now().month,
    #                               datetime.now().day, 
    #                               datetime.now().hour, 
    #                               datetime.now().minute, 
    #                               datetime.now().second
    #                             )
    #         for task, cron_expression in self.tasks:
    #             cron = croniter(cron_expression, current_time)
    #             next_run_time = cron.get_next(datetime)
    #             last_run_time = cron.get_prev(datetime)
    #             logging.debug(f"Current Time: {current_time}, Next Run Time: {next_run_time}")
    #             if next_run_time == current_time or current_time == last_run_time:
    #                 logging.info("Queuing Task")
    #                 await self.queue.enqueue_task(task)
    #             else:
    #                 logging.debug("Not Time")
    #         await asyncio.sleep(1)
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