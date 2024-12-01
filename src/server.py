import random
import socket
import threading
import uuid
from src.logger import info, error
from settings import PORT, IP, MOTD, SERVER_NAME
from src.constants import AREA_TREES, PING, LOAD, GAME_COMMANDS, CHECK_GAME, GET_AREA, UNLOAD, CHAT

class Server:
    def __init__(self, world):
        self.world = world
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORT))
        self.socket.listen(5)
        self.client_threads = []
        self.stop_event = threading.Event()  # Event to signal server shutdown
        self.players = []

    def add_player(self, name, uuid, x, y):
        self.players.append({"name": name, "uuid": uuid, "x": x, "y": y})

    def start(self):
        info(f"Server started and listening on {IP}:{PORT}")

    def step(self):
        try:
            self.socket.settimeout(1.0)  # Non-blocking with timeout
            client, address = self.socket.accept()
            if self.stop_event.is_set():  # Check if we should stop
                return
            # info(f"Client connected from {address[0]}:{address[1]}")
            client_thread = threading.Thread(target=self.client_thread, args=(client, address))
            client_thread.start()
            self.client_threads.append(client_thread)
        except socket.timeout:
            pass

    def client_thread(self, client, address):
        NONE = -1
        PING = 0
        PLAYER = 1
        mode = NONE
        try:
            while not self.stop_event.is_set():  # Exit loop if stop event is set
                event = self._receive_data(client, 4)
                if not event:
                    break
                event_type = int.from_bytes(event, byteorder='big')
                
                if event_type == PING:
                    self._send_data(client, MOTD.encode())
                    self._send_data(client, SERVER_NAME.encode())


                elif event_type == LOAD:
                    self._join_event(client, address)

                # when players disconnects
                elif event_type == UNLOAD:
                    player_name = self._receive_data(client, 1024).decode().strip()
                    if mode == PING:
                        pass
                    elif mode == PLAYER:
                        info(f"Player {player_name} disconnected")
                    else:
                        info("!!! Someone is pinging the server without permission !!!")

                # to be honest i dont know
                elif event_type == GAME_COMMANDS:
                    command = self._receive_data(client, 1024).decode().strip()
                    info(f"Received command: {command}")

                # when clientg pings the server
                elif event_type == CHECK_GAME:
                    info(f"{address} pinged the server")
                    # game checks every 10s localhosts this is used to detect if it the localhost (this server) is designed for this server
                    self._send_data(client, f"rc".encode()) 


                elif event_type == GET_AREA:
                    self._get_area_event(client)

                    
                elif event_type == CHAT:
                    self._handle_chat_event(client)

                elif event_type == AREA_TREES:
                    self._send_area_trees(client)




                    


                else:
                    info(f"Received unknown event: {event_type}")
        except Exception as e:
            error(f"Error handling client {address[0]}:{address[1]}: {e}")
        finally:
            self.disconnect_player(client)

    def _join_event(self, client, address):
        player_name = self._receive_data(client, 1024).decode().strip()
        player_uuid = f"{socket.gethostbyname(socket.gethostname())}_{address[1]}"
        self.add_player(player_name, player_uuid, 0, 0)
        self._send_data(client, f"Welcome to the server {player_name}!".encode())
        info(f"Player {player_name} joined")
    
    def _handle_chat_event(self, client):
        message = self._receive_data(client, 1024).decode().strip()
        self._send_data(client, f"{message}".encode())
        info(f"Received chat message: {message}")

    def _get_area_event(self, client):
        area_size = 16
        x = self._receive_data(client, 4)
        y = self._receive_data(client, 4)
        

        x = int.from_bytes(x, byteorder='big')
        y = int.from_bytes(y, byteorder='big')
        
        section = self.world.get_section(x, y, area_size)
        
        for row in section:
            for value in row:
                self._send_data(client, value.to_bytes(4, byteorder='big'))

    def _send_area_trees(self, client):
        random_trees = [
            random.randint(0, 100) for _ in range(100)
        ]
        self._send_data(client, len(random_trees).to_bytes(4, byteorder='big'))

        for tree in random_trees:
            self._send_data(client, tree.to_bytes(4, byteorder='big'))

    def _receive_data(self, client, size):
        try:
            data = client.recv(size)
            if not data:
                pass
            return data
        except socket.error as e:
            error(f"Socket error: {e}")
            raise

    def _send_data(self, client, data):
        try:
            client.sendall(data)
        except socket.error as e:
            error(f"Socket error: {e}")

    def disconnect_player(self, client):
        client.close()
        

    def close(self):
        info("Server shutting down...")
        self.stop_event.set()  # Signal all threads to stop
        self.socket.close()
        
        for thread in self.client_threads:
            thread.join()  # Wait for all threads to finish
        
        info("All client threads have been terminated. Server shutdown complete.")
