import socket
import threading
import re
from plugins.plugin import Ex

import os
import socket
import threading
from src.logger import plugin
import re

class Plugin(Ex):  # Inheriting from the base Plugin class
    def __init__(self):
        super().__init__("web")  # Initialize the base class
        self.server_socket = None

    def info(self, text):
        plugin(text, self.plugin_name)

    def onLoad(self) -> None:
        """Called when the plugin is loaded"""
        super().info("Web Plugin is loaded")
        threading.Thread(target=self.run_web_server, daemon=True).start()  # Run the web server in a new thread

    def onUnload(self) -> None:
        """Called when the plugin is unloaded"""
        super().info("Web Plugin is unloaded")
        if self.server_socket:
            self.server_socket.close()

    def run_web_server(self):
        """Sets up and runs the web server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 8080))  # Binding to localhost:8080
        self.server_socket.listen(5)
        self.info("Web server is running on port 8080")

        while True:
            client_socket, addr = self.server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            self.handle_request(client_socket, request)


    def handle_request(self, client_socket, request):
        """Handles incoming requests and serves appropriate responses"""
        route = self.get_route(request)
        if route == "/":
            response = self.get_home_screen()
            self.info("Returning home screen")
        elif route == "/log":
            import json
            log_content = self.getLastMessage()  # Should return a dictionary
            log_content_json = json.dumps(log_content)  # Convert to JSON string
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json; charset=UTF-8\r\n"
                "Connection: close\r\n\r\n"
                f"{log_content_json}"
            )
        else:
            response = "HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n"

        # Send response to client
        client_socket.sendall(response.encode('utf-8'))
        client_socket.shutdown(socket.SHUT_WR)  # Ensure data is fully sent before closing
        client_socket.close()


    def get_home_screen(self):
        """Generates a simple home screen HTML"""
        response = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #121212;
            color: #e0e0e0;
        }

        header {
            background-color: #1e1e1e;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-bottom: 1px solid #333;
        }

        main {
            padding: 20px;
        }

        .server-info {
            display: flex;
            flex-direction: column;
            position: relative;
            gap: 10px;
            background: #1e1e1e;
            height: 200px;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #333;
            margin-bottom: 20px;
        }

        .server-info button {
            padding: 0;
            background-color: #f44336;
            width: 100px;
            height: 100px;
            color: #ffffff;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            position: absolute;
            right: 20px; /* Move the button to the right */
            top: 50%;    /* Center vertically within the div */
            transform: translateY(-50%); /* Adjust for exact vertical centering */
        }

        .server-info .name {
            font-weight: bold;
            font-size: 30px;
        }

        .server-info .motd {
            font-weight:50;
            color: gray; 
        }

        .server-info .count {
            position: absolute;
            bottom: 15px;
        }

        .server-info button:hover {
            background-color: #d32f2f;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            font-size: 18px;
        }

        #log-container {
            background: #1e1e1e;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 5px;
            height: 300px;
            overflow-y: auto;
            font-family: monospace;
        }

        #log-container p {
            margin: 0;
            padding: 5px 0;
            border-bottom: 1px solid #333;
        }

        #log-container p:last-child {
            border-bottom: none;
        }

        .info strong {
            color: #4fc3f7;
        }

        .error strong {
            color: #f44336;
        }

        .plugin strong {
            color: #8bc34a;
        }

        .gray {
            color: #9e9e9e;
        }

        .white {
            color: #e0e0e0;
        }

        .command-input {
            width: 100%;
            padding: 10px;
            background-color: #2c2c2c;
            border: 1px solid #444;
            color: #e0e0e0;
            border-radius: 5px;
            font-size: 16px;
            margin: 15px 0px;
            box-sizing: border-box; /* Ensures padding is included in the element's total width/height */
            resize: none; /* Prevents resizing of the input box */
        }

        .command-input:focus {
            outline: none;
            border-color: #4fc3f7;
        }
    </style>
</head>
<body>
    <header>
        <div class="server-info">
            <div class="info-item name">
                <span id="server-name">My Awesome Server</span>
            </div>
            <div class="info-item motd">
                <span id="server-motd">Welcome to the server!</span>
            </div>
            <div class="info-item count">
                <span id="player-count">0/?</span>
            </div>
            <button onclick="stopServer()">Stop</button>
        </div>
    </header>
    <main>
        <h2>Log Viewer</h2>
        <div id="log-container"></div>
        <input type="text" id="command-input" class="command-input" placeholder="Type a command..." onkeydown="handleCommand(event)">
    </main>

    <script>
        let lastLog = "";
        let logCount = 0;

        async function fetchLog() {
            try {
                const response = await fetch('http://localhost:8080/log');
                const logContent = await response.text();

                // Parse logContent as JSON
                const logData = JSON.parse(logContent);

                if (lastLog !== logData.text) {
                    appendLog(logData);
                    lastLog = logData.text;
                }
            } catch (error) {
                console.error("Error fetching or parsing log:", error);
            }
        }

        function appendLog(logData) {
            const logContainer = document.getElementById('log-container');

            // Generate log message with styling
            let logMessage = `<span class="gray">[${logData.time}]</span> `;
            if (logData.type === 0) {
                logMessage += `<strong class="info">[INFO]</strong> `;
            } else if (logData.type === 1) {
                logMessage += `<strong class="error">[ERROR]</strong> `;
            } else if (logData.type === 2) {
                logMessage += `<strong class="plugin">[PLUGIN]</strong> `;
            }
            logMessage += `<span class="gray">[${logData.file}]</span> `;
            logMessage += `<span class="white">${logData.text}</span>`;

            // Create a log entry
            const logEntry = document.createElement('p');
            logEntry.innerHTML = logMessage;

            // Append to the log container
            logContainer.appendChild(logEntry);

            // Scroll to the latest log
            logContainer.scrollTop = logContainer.scrollHeight;
        }

        function stopServer() {
            alert("Stopping the server...");
            // Implement the server stop logic here
        }

        function handleCommand(event) {
            if (event.key === 'Enter') {
                const command = document.getElementById('command-input').value;
                console.log("Command entered:", command);
                // Implement command processing logic here (e.g., send to server)

                // Clear the input box
                document.getElementById('command-input').value = '';
            }
        }

        // Fetch logs every 200 milliseconds
        setInterval(fetchLog, 200);
    </script>
</body>
</html>






"""
        return response

    def handle_last_message(self, log_line):
        return log_line

    def get_route(self, request):
        """Parses the route from the incoming request"""
        try:
            route = request.split(" ")[1]
        except IndexError:
            route = "/"
        return route

    def step(self) -> None:
        """Called every step in main loop (empty or custom logic)"""
        pass
