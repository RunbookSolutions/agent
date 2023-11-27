from runbooksolutions.agent.PluginManager import PluginManager
from runbooksolutions.agent.Task import Task
from threading import Event
import logging
import asyncio

class Queue:
    def __init__(self, num_threads: int = 1, pluginManager: PluginManager = None) -> None:
        self.task_queue = asyncio.Queue()
        self.num_threads = num_threads
        self.threads = []
        self.stop_event = Event()
        self.pluginManager = pluginManager

    def _worker(self):
        while not self.stop_event.is_set():
            try:
                task = self.task_queue.get_nowait()
                self.execute_task(task)
            except asyncio.QueueEmpty:
                pass
            except asyncio.CancelledError:
                # Log a message when the coroutine is canceled
                logging.debug("Worker coroutine canceled.")
                break
            except Exception as e:
                logging.error(e)
                pass  # Handle exceptions as needed

    def execute_task(self, task: Task) -> None:

        command = task.command
        arguments = task.getArguments()

        # Implement your task execution logic here
        logging.info(f"Running Task \'{command}\' with arguments {arguments}")
        self.pluginManager.executeCommand(command, **arguments)
        pass

    async def start(self) -> None:
        logging.debug("Queue Started")
        try:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(None, self._worker) for _ in range(self.num_threads)]
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logging.info("Received KeyboardInterrupt. Stopping gracefully.")
        finally:
            self.stop()

    def stop(self) -> None:
        self.stop_event.set()

    async def enqueue_task(self, task: Task) -> None:
        task_id = task.id
        if not self._is_task_in_queue(task_id):
            logging.debug("Enqueued Task")
            await self.task_queue.put(task)
        else:
            logging.warning("Task already in Queue.")

    def _is_task_in_queue(self, task_id: str) -> bool:
        for task in self.task_queue._queue:
            if task.id == task_id:
                return True
        return False
