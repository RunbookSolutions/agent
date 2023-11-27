
import logging
from runbooksolutions.logging_setup import setup_logging
setup_logging()


from runbooksolutions.store.Store import Store
# Set the Data Store(s) Password
Store.set_encryption_key(b"Store_Encryption_Password")
from runbooksolutions.agent.Agent import Agent

async def main():
    agent = Agent(num_threads=3)
    try:
        await agent.start()
    except KeyboardInterrupt:
        logging.info("Received CTRL+C. Stopping gracefully.")
        await agent.stop()

import asyncio
if __name__ == "__main__":
    asyncio.run(main())