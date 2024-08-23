from src.logger import plugin
import os
import config as cfg


class Ex:
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name
        self.game_command_list = []
        self.console_command_list = []
        self.last_message = ""
        # the command list has structure 

    def info(self, text):
        plugin(text, self.plugin_name)

    def getLastMessage(self) -> str:
        """Returns last message from console"""
        return self.last_message

    def createConsoleCommand(self, command: callable, command_name: str, args: list) -> int:
        """Adds a function to the terminal (this command doesn't work in game, just in console and still doesnt work)

        :param command: The function to be called when the command is entered
        :type command: callable

        :return: 0 if the command was added successfully, 1 otherwise
        :rtype: int
        """
        # self.command_list.append({"command_name": command_name,"args": [], "func": command})
        return 0 | 1;

    def createGameCommand(self, command: callable, args: list, command_name: str) -> int:
        """Adds a function to the game (not to the console, just in the game)

        :param command: The function to be called when the command is entered
        :type command: callable
        :param args: The arguments of the command
        :type args: list
        :param command_name: The name of the command
        :type command_name: str

        :return: 0 if the command was added successfully, 1 otherwise
        :rtype: int
        """
        self.game_command_list.append({"command_name": command_name,"args": args, "func": command})
        return 0 | 1
    
    def onLoad(self) -> None:
        """Calls when the plugin is loaded"""
        return None
    
    def onUnload(self) -> None:
        """Calls when the plugin is unloaded (still in development so it's not called)"""

    def step(self) -> None:
        """Calls every step in main loop"""
        pass

    def generateFolder(self) -> None:
        """If not generated already it will generate folder for the plugin in plugins folder"""
        if not os.path.exists("plugins/" + self.plugin_name):
            os.mkdir("plugins/" + self.plugin_name)
        else:
            return None

    def generateConfig(self, config_name="") -> None:
        """If not generated already it will generate config file for the plugin in plugins folder"""
        if config_name == "":
            config_name = self.plugin_name
        # check if plugin folder already exists
        self.generateFolder()

        if not os.path.exists("plugins/" + self.plugin_name + "/" + config_name + ".cfg"):
            with open("plugins/" + self.plugin_name + "/" + config_name + ".cfg", "w") as f:
                f.write("")
        else:
            return None

    