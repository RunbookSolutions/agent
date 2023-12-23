from modules.interfaces import APIInterface, AuthInterface, RawPluginInterface, TaskInterface

class API(APIInterface):
    def __init__(self, auth: AuthInterface) -> None:
        self._auth = auth

    def getAgent(self) -> None:
        return super().getAgent()
    
    def getPlugin(self, id: str) -> RawPluginInterface:
        return super().getPlugin(id)
    
    def getTasks(self) -> [TaskInterface]:
        return super().getTasks()
    
    def putTaskResult(self, id: str, result: any) -> bool:
        return super().putTaskResult(id, result)
    
    def makeRequest(self, request, data) -> any:
        return super().makeRequest(request, data)