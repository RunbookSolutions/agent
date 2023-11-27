from runbooksolutions.agent.Plugin import Plugin
from runbooksolutions.agent.API import API
import json
import logging
import os
import importlib
import hashlib

class PluginManager:
    plugin_directory: str = "plugins"
    plugins: dict = dict()
    loadedCommands: dict = dict()
    api: API = None

    def __init__(self, api: API) -> None:
        self.api = api

    def verify_plugin_hash(self, pluginID: str) -> bool:
        json_file_path = os.path.join(self.plugin_directory, f"{pluginID}.json")
        with open(json_file_path, 'r') as json_file:
            plugin_definition = json.loads(json_file.read())

        script = plugin_definition.get('script', '').encode('utf-8')
        json_hash = hashlib.sha512(script).hexdigest()

        script_file_path = os.path.join(self.plugin_directory, f"{pluginID}.py")
        with open(script_file_path, 'rb') as script_file:
            script_content = script_file.read()
            script_hash = hashlib.sha512(script_content).hexdigest()

        logging.debug(f"Expected Hash: {plugin_definition.get('hash')}")
        logging.debug(f"JSON Hash: {json_hash}")
        logging.debug(f"JSON Hash: {script_hash}")

        if not json_hash == plugin_definition.get('hash', ''):
            logging.critical("JSON Hash mismatch")
            return False

        if not script_hash == plugin_definition.get('hash', ''):
            logging.critical("SCRIPT Hash mismatch")
            return False
        
        return True
    
    def addPlugin(self, pluginID: str) -> None:
        logging.debug(f"Adding Plugin {pluginID}")
        if self.pluginIsLocal(pluginID):
            logging.debug("Plugin is local")
        else:
            self.downloadPlugin(pluginID)

        if not self.verify_plugin_hash(pluginID):
            logging.critical(f"Plugin {pluginID} FAILED Hash Verification")
            return
        
        self.plugins[pluginID] = self.loadPlugin(pluginID)
        self.loadPluginCommands(pluginID)

    def removePlugin(self, pluginID: str) -> None:
        logging.debug(f"Removing Plugin {pluginID}")
        if pluginID in self.plugins:
            del self.plugins[pluginID]
        else:
            logging.warning(f"Plugin {pluginID} not found in loaded plugins.")

        # TODO: Remove the plugin files from the file system
        json_file_path = os.path.join(self.plugin_directory, f"{pluginID}.json")
        with open(json_file_path, 'r') as json_file:
            plugin_definition = json.load(json_file)

        for command in plugin_definition.get('commands', []).keys():
            self.loadedCommands.pop(command)

    def syncPlugins(self, plugins: list) -> None:
        logging.debug(f"Syncing Plugins. Loaded Plugins: {list(self.plugins.keys())} Requested Plugins: {plugins}")
        for pluginID in self.plugins.keys():
            if pluginID not in plugins:
                logging.debug("Removing Plugin")
                self.removePlugin(pluginID)
            else:
                logging.debug("Plugin Still Required.")

        for pluginID in plugins:
            if pluginID not in self.plugins.keys():
                logging.debug("Adding Plugin")
                self.addPlugin(pluginID)
            else:
                logging.debug("Plugin Already Loaded")

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
        pluginData = self.api.sendRequest(f'/agent/plugin/{pluginID}', 'GET')
        pluginData = pluginData.get('data')
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

        commands = plugin_definition.get('commands', [])

        for command_name, command_data in commands.items():
            modified_command = {'pluginID': pluginID, **command_data}

            self.loadedCommands.update({command_name: modified_command})

    def executeCommand(self, commandName, *args, **kwargs) -> None:
        if not self.commandIsLoaded(commandName):
            logging.critical(f"Tried to call {commandName} when it wasn't loaded")
            return

        pluginID = self.loadedCommands.get(commandName).get('pluginID')
        function_name = self.loadedCommands.get(commandName).get('function')

        function_to_call = getattr(self.plugins.get(pluginID), function_name, None)
        if callable(function_to_call):
            function_to_call(*args, **kwargs)
        else:
            print(f"Function {function_name} not found in plugin {pluginID}.")