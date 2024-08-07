# server.py
import socket
import threading
from src.logger import info, error
from settings import PORT, IP, MOTD, MAX_PLAYERS, MAX_PLAYERS_PER_IP, MAX_PLAYERS_PER_NAME, MAX_PLAYERS_PER_UUID, MAX_PACKETS_PER_TICK, SERVER_NAME
from src.constants import PING, LOAD, UNLOAD, GAME_VERSION, SERVER_VERSION, GAME_COMMANDS

class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((IP, PORT))
        self.socket.listen(5)
        self.client_threads = []

    def start(self):
        info(f"Server started and listening on {IP}:{PORT}")

    def step(self):
        try:
            self.socket.settimeout(1.0)  # Non-blocking with timeout
            client, address = self.socket.accept()
            info(f"Client connected from {address[0]}:{address[1]}")
            client_thread = threading.Thread(target=self.client_thread, args=(client, address))
            client_thread.start()
            self.client_threads.append(client_thread)
        except socket.timeout:
            pass

    def new_player(self, client, address):
        pass
    def client_thread(self, client, address):
        try:
            while True:
                event = client.recv(4)
                player_id = client.recv(8)
                player_id = int.from_bytes(id, byteorder='big')
                if not event:
                    break
                event_type = int.from_bytes(event, byteorder='big')
                info("player id: " + player_id + " requested event: " + event_type)
                if event_type == PING:
                    client.send(MOTD.encode())
                    info("Sending MOTD")
                    client.send(SERVER_NAME.encode())
                    info("Sending Server Name")
                elif event_type == LOAD:
                    player_name = client.recv(1024).decode()
                    client.send(f"Welcome to the server {player_name}!".encode())
                    info(f"Player {player_name} joined")
                elif event_type == GAME_COMMANDS:
                    command = client.recv(1024).decode()
                    info(f"Received command: {command}")
                else:
                    info(f"Received unknown event: {event}")
        except Exception as e:
            error(f"Error handling client {address[0]}:{address[1]}: {e}")
        finally:
            self.disconnect_player(client)

    def disconnect_player(self, client):
        client.close()
        info("Client disconnected")

    def close(self):
        self.socket.close()
        for thread in self.client_threads:
            thread.join()
        info("Shutting down server...")
