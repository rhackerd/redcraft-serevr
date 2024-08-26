import threading
import sys
import signal
import time  # Add this for loop delays
from src.server import Server
from src.console import Console
from src.mod_sys import Mod_sys
from settings import PORT, IP, MOTD, MAX_PLAYERS, MAX_PLAYERS_PER_IP, MAX_PLAYERS_PER_NAME, MAX_PLAYERS_PER_UUID, MAX_PACKETS_PER_TICK
from src.commands import Commands
import src.logger

class MainApp:
    def __init__(self):
        self.server = Server()
        self.console = Console()
        self.mod_sys = Mod_sys()
        self.plugins = []
        self.broken_plugins = []
        self.commands = Commands()
        self.stop_event = threading.Event()  # Event to signal threads to stop

    def start(self):
        src.logger.info("Starting server...")
        src.logger.info("Checking plugins")
        self.mod_sys.check_all_plugins()
        src.logger.info("We recommend using the web plugin for now, console is a little bit broken")
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

        # Start console and plugin loop in separate threads
        self.console.do_plugins = self.show_plugins

        plugin_thread = threading.Thread(target=self.plugin_loop)
        plugin_thread.start()

        console_thread = threading.Thread(target=self.console_loop)
        console_thread.start()

        src.logger.info("Console listener started")

        try:
            while not self.stop_event.is_set():
                self.server.step()
                time.sleep(0.1)  # Add small sleep to reduce CPU usage and allow responsive exit
        except KeyboardInterrupt:
            pass
        finally:
            src.logger.info("Shutting down the server.")
            self.mod_sys.shutdown()
            self.shutdown()
            src.logger.info("Server shutdown complete.")
            src.logger.info("!!!! &<red>&ltype exit to fully shutdown server &<white>&l!!!!")

    def shutdown(self):
        self.stop_event.set()  # Signal all threads to stop
        self.server.close()

        # Give threads a chance to finish
        time.sleep(1)

        src.logger.info("Waiting for thread to finish...")

    def show_plugins(self, arg):
        src.logger.info("Plugins:")
        for p in self.plugins:
            src.logger.info(f"- &<green>&l{p}&r")
        for p in self.broken_plugins:
            src.logger.info(f"- &<red>&l{p}&r")

    def load_all_plugins(self):
        self.mod_sys.load_all_plugins()

    def console_loop(self):
        while not self.stop_event.is_set():
            self.console.cmdloop()
            time.sleep(0.1)  # Allow loop to exit promptly

    def plugin_loop(self):
        try:
            while not self.stop_event.is_set():
                self.mod_sys.step()
                for i in self.mod_sys.plugins:
                    i.last_message = src.logger.last_log
                time.sleep(0.1)  # Allow loop to exit promptly
        except KeyboardInterrupt:
            pass

    def on_exit(self):
        src.logger.info("Exit command received. Closing server...")
        self.server.close()

def signal_handler(sig, frame):
    app.shutdown()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Handle Ctrl+C gracefully
    app = MainApp()
    app.start()