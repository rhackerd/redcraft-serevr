from src.logger import info, error

class Commands:
    def __init__(self):
        self.server_commands = []
        self.client_commands = []

    def runCommand(self, command):
        pass

    def runGameCommand(self, command):
        pass

    def runConsoleCommand(self, command):
        pass

    def getAllGameCommands(self):
        pass

    def getAllConsoleCommands(self):
        pass

    def getAllGameAndConsoleCommands(self):
        pass

    def getAllCommands(self):
        return 0;

    def setServerCommands(self, arg):
        pass

    def setClientCommands(self, arg):
        pass