from runbooksolutions.agent.Plugin import Plugin
from runbooksolutions.agent.API import API
import json
import logging
import os
import importlib

class PluginManager:
    plugin_directory: str = "plugins"
    plugins: dict = dict()
    loadedCommands: dict = dict()
    api: API = None

    def __init__(self, api: API) -> None:
        self.api = api

    def addPlugin(self, pluginID: str) -> None:
        logging.debug(f"Adding Plugin {pluginID}")
        if self.pluginIsLocal(pluginID):
            logging.debug("Plugin is local")
        else:
            self.downloadPlugin(pluginID)
        
        self.plugins[pluginID] = self.loadPlugin(pluginID)
        self.loadPluginCommands(pluginID)

    def removePlugin(self, pluginID: str) -> None:
        pass

    def syncPlugins(self, plugins: list) -> None:
        pass

    def pluginIsLocal(self, pluginID: str) -> bool:
        if not os.path.exists(os.path.join(self.plugin_directory, f"{pluginID}.json")):
            logging.debug("Plugin JSON Not Local")
            return False
        
        if not os.path.exists(os.path.join(self.plugin_directory, f"{pluginID}.py")):
            logging.debug("Plugin python Not Local")
            return False
        
        return True
    
    def downloadPlugin(self, pluginID: str) -> None:
        logging.debug(f"Downloading Plugin {pluginID}")
        pluginData = self.api.sendRequest('http://192.168.1.197/api/agent/plugins/download', 'GET')
        self.savePlugin(pluginData)
    
    def savePlugin(self, plugin_definition: dict) -> None:
        logging.debug("Saving Plugin")
        if not os.path.exists(self.plugin_directory):
            os.makedirs(self.plugin_directory)

        # Save JSON data
        json_file_path = os.path.join(self.plugin_directory, f"{plugin_definition.get('id')}.json")
        with open(json_file_path, 'w') as json_file:
            json.dump(plugin_definition, json_file)

        # Save Python script
        script_file_path = os.path.join(self.plugin_directory, f"{plugin_definition.get('id')}.py")
        with open(script_file_path, 'w') as script_file:
            script_file.write(plugin_definition.get('script', ''))

    def commandIsLoaded(self, commandName: str) -> bool:
        if commandName in self.loadedCommands.keys():
            return True
        return False
    
    def loadPlugin(self, pluginID: str) -> Plugin:
        try:
            script_file_path = os.path.join(self.plugin_directory, f"{pluginID}.py")
            spec = importlib.util.spec_from_file_location("Plugin", script_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Store the instance of the plugin in the loaded_plugins dictionary
            return module.Plugin()
        except Exception as e:
            print(f"Error importing plugin {pluginID}: {e}")
            return None
        
    def loadPluginCommands(self, pluginID: str) -> None:
        json_file_path = os.path.join(self.plugin_directory, f"{pluginID}.json")
        with open(json_file_path, 'r') as json_file:
            plugin_definition = json.load(json_file)
        self.loadedCommands.update(plugin_definition.get('commands', []))

    def executeCommand(self, commandName, *args, **kwargs) -> None:
        if not self.commandIsLoaded(commandName):
            logging.critical(f"Tried to call {commandName} when it wasn't loaded")
            return

        function_name = self.loadedCommands.get(commandName).get('function')

        function_to_call = getattr(self.plugins.get('123456789'), function_name, None)
        if callable(function_to_call):
            function_to_call(*args, **kwargs)
        else:
            print(f"Function {function_name} not found in plugin {"123456789"}.")