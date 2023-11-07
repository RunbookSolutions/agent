# app.py
import asyncio
from agent.agent import Agent
import configparser

async def main():
    agent = Agent()

    config = configparser.ConfigParser()
    config.read('plugins.ini')

    for section_name in config.sections():
        plugin = {}
        plugin['name'] = section_name
        plugin['options'] = dict(config.items(section_name))
        if config.getboolean(section_name, 'enabled'):
            await agent.add_plugin_by_name(plugin)

    try:
        await agent.start()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping the agent...")
        await agent.stop()
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())
