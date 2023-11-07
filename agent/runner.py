# agent/runner.py
import threading

# Function that simulates a task that threads will execute
def worker_thread(thread_id, data_queue, agent):
    while True:
        # Poll for tasks to run (e.g., from a task queue)
        event = data_queue.get()  # Get data from the queue
        if event is None:  # Exit condition
            break

        agent.handle_event(event)

class Runner:
    concurrency_limit = 1

    def __init__(self, data_queue, agent_instance):
        self.data_queue = data_queue
        self.agent = agent_instance
        self.thread_group = []

    def start(self):
        for i in range(self.concurrency_limit):
            thread = threading.Thread(target=worker_thread, args=(i, self.data_queue, self.agent))
            thread.daemon = True  # Mark threads as daemon to exit when the main program exits
            self.thread_group.append(thread)
            thread.start()

    def join(self):
        for thread in self.thread_group:
            thread.join()

    def stop(self):
        # Signal the worker threads to exit by adding None to the data queue
        for _ in range(self.concurrency_limit):
            self.data_queue.put(None)