from runbooksolutions.agent.PluginManager import PluginManager
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

    def execute_task(self, task: dict) -> None:
        # Implement your task execution logic here
        logging.error(f"Running Task {task}")
        self.pluginManager.executeCommand('lol', 2)
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

    async def enqueue_task(self, task: dict) -> None:
        logging.debug("Enqueued Task")
        await self.task_queue.put(task)
