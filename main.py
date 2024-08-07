from src.server import Server
from src.console import Console
import threading
from src.mod_sys import Mod_sys
from settings import PORT, IP, MOTD, MAX_PLAYERS, MAX_PLAYERS_PER_IP, MAX_PLAYERS_PER_NAME, MAX_PLAYERS_PER_UUID, MAX_PACKETS_PER_TICK
from src.commands import Commands
import sys
import src.logger

class MainApp:
    def __init__(self):
        self.server = Server()
        self.console = Console()
        self.mod_sys = Mod_sys()
        self.plugins = []
        self.broken_plugins = []
        self.commands = Commands()

    def start(self):
        src.logger.info("Starting server...")
        src.logger.info("checking plugins")
        self.mod_sys.check_all_plugins()
        src.logger.info("we recommend using web plugin for now, console is a little bit broken")
        self.load_all_plugins()
        for p in self.mod_sys.plugins:
            self.plugins.append(p.plugin_name)
            self.commands.setClientCommands(p.game_command_list)
            self.commands.setServerCommands(p.console_command_list)
        for test in self.mod_sys.broken_plugins:
            self.broken_plugins.append(test)
        self.mod_sys.configManager()
        self.server.start()
        src.logger.info("Server started and listening on port 8080")

        # Start console loop in a separate thread
        self.console.do_plugins = self.show_plugins

        plugin_thread = threading.Thread(target=self.plugin_loop)
        plugin_thread.start()

        console_thread = threading.Thread(target=self.console_loop)
        console_thread.start()

        src.logger.info("Console listener started")

        try:
            while True:
                self.server.step()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.close()
            src.logger.info("Shutting down server...")
            for x in self.mod_sys.plugins:
                x.onUnload()
            plugin_thread.join()
            console_thread.join()
            sys.exit(0)

    def show_plugins(self, arg):
        src.logger.info("Plugins:")
        for p in self.plugins:
            src.logger.info(f"- &<green>&l{p}&r")
        for p in self.broken_plugins:
            src.logger.info(f"- &<red>&l{p}&r")


    def load_all_plugins(self):
        self.mod_sys.load_all_plugins()

    def console_loop(self):
        self.console.cmdloop()

    def plugin_loop(self):
        try:
            while True:
                self.mod_sys.step()
                for i in self.mod_sys.plugins:
                    i.last_message = src.logger.last_log
        except KeyboardInterrupt:
            pass

    def on_exit(self):
        src.logger.info("Exit command received. Closing server...")
        self.server.close()

if __name__ == "__main__":
    app = MainApp()
    app.start()
