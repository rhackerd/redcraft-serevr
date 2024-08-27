import socket
import threading
from src.logger import info, error
from settings import PORT, IP, MOTD, SERVER_NAME
from src.constants import PING, LOAD, GAME_COMMANDS, CHECK_GAME, GET_AREA

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((IP, PORT))
        self.socket.listen(5)
        self.client_threads = []
        self.stop_event = threading.Event()  # Event to signal server shutdown

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
                    player_name = self._receive_data(client, 1024).decode().strip()
                    self._send_data(client, f"Welcome to the server {player_name}!".encode())
                    info(f"Player {player_name} joined")
                elif event_type == GAME_COMMANDS:
                    command = self._receive_data(client, 1024).decode().strip()
                    info(f"Received command: {command}")
                elif event_type == CHECK_GAME:
                    # game checks every 10s localhosts this is used to detect if it the localhost (this server) is designed for this server
                    self._send_data(client, f"rc".encode()) 
                elif event_type == GET_AREA:
                    x = self._receive_data(client, 4)
                    y = self._receive_data(client, 4)
                    self._send_data(client, f"{x},{y}".encode())
                else:
                    info(f"Received unknown event: {event_type}")
        except Exception as e:
            error(f"Error handling client {address[0]}:{address[1]}: {e}")
        finally:
            self.disconnect_player(client)

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
