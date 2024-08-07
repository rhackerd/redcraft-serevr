from plugins.plugin import Ex
import socket
import threading

class Plugin(Ex):
    def __init__(self):
        super().__init__("web")
        self.createGameCommand(lambda: print("hello from console"), ["test"], "test")
        self.server_socket = None

    def onLoad(self):
        super().info("plugin is loaded")

        # Run the web server in a separate thread
        threading.Thread(target=self.run_web_server, daemon=True).start()

    def run_web_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 8080))
        self.server_socket.listen(5)
        self.info("Socket web server is running on port 8080")

        while True:
            client_socket, addr = self.server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            self.handle_request(client_socket, request)

    def handle_request(self, client_socket, request):

        route = self.getRoute(request)
        if route == "/":
            response = self.getHomeScreen()
            self.info("Returning home screen")
        elif route == "/log":
            response = self.getLastMessage()
        else:
            response = "404 Not found"
    
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def getHomeScreen(self):
        response = """\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
<head>
    <title>Simple Web Server</title>
</head>
<body>
    <div id="response"></div>

    <script>
        let previousResponse = '';
        let element = document.getElementById("response");

        function addText(text) {
            element.innerHTML += "<p>"+text+"</p>";
        }
        async function checkForUpdates() {
            try {
                const response = await fetch('/log');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const currentResponse = await response.text();
                if (currentResponse !== previousResponse) {
                    console.log('Response changed');
                    addText(currentResponse);
                    previousResponse = currentResponse;
                }
            } catch (error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        }

        // Check for updates every 1 millisecond
        setInterval(checkForUpdates, 1);
    </script>
</body>
</html>
"""
        return response



    def getRoute(self, request):
        try:
            route = str(request).split(" ")[1]
        except IndexError:
            route = "Error finding route!"
        return route

    def step(self):
        pass
        # Custom logic here, for example:
        # while True:
        #     print("Running custom loop")
        #     time.sleep(5)

    def onUnload(self):
        super().info("plugin is unloaded")
        if self.server_socket:
            self.server_socket.close()

# Simulated plugin loading and running for demonstration purposes
