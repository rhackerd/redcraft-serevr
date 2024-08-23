from plugins.plugin import Ex
import socket
import threading
import re

class Plugin(Ex):
    def __init__(self):
        super().__init__("web")
        self.generateFolder()
        self.generateConfig()
        self.createGameCommand(lambda: print("hello from console"), ["test"], "test")
        self.server_socket = None

    def onLoad(self):
        super().info("plugin is loaded")

        # Run the web server in a separate thread
        threading.Thread(target=self.run_web_server, daemon=True).start()

    def run_web_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 8080))
        self.server_socket.listen(5)
        self.info("Socket web server is running on port 8080")

        while True:
            client_socket, addr = self.server_socket.accept()
            request = client_socket.recv(1024).decode('utf-8')
            self.handle_request(client_socket, request)

    def handleSequences(self, sequence):
        if sequence == "0":
            return "reset"
        elif sequence == "1":
            return "bold"
        elif sequence == "2":
            return "dim"
        elif sequence == "3":
            return "italic"
        elif sequence == "4":
            return "underline"
        elif sequence == "5":
            return "blink"
        elif sequence == "6":
            return "fastBlink"
        elif sequence == "7":
            return "reverse"
        elif sequence == "8":
            return "conceal"
        elif sequence == "9":
            return "crossed"
        elif sequence == "30":
            return "black"
        elif sequence == "31":
            return "red"
        elif sequence == "32":
            return "green"
        elif sequence == "33":
            return "yellow"
        elif sequence == "34":
            return "blue"
        elif sequence == "35":
            return "magenta"
        elif sequence == "36":
            return "cyan"
        elif sequence == "37":
            return "white"
        elif sequence == "90":
            return "brightBlack"
        elif sequence == "91":
            return "brightRed"
        elif sequence == "92":
            return "brightGreen"
        elif sequence == "93":
            return "brightYellow"
        elif sequence == "94":
            return "brightBlue"
        elif sequence == "95":
            return "brightMagenta"
        elif sequence == "96":
            return "brightCyan"
        elif sequence == "97":
            return "brightWhite"


    def handleLastMessage(self, log_line):
        # Define color mapping
        color_map = {
            '30': 'gray',        # ANSI code for black
            '31': 'red',
            '32': 'green',
            '33': 'yellow',
            '34': '#346DC8',
            '35': 'magenta',
            '36': 'cyan',
            '37': 'white',
            '0': 'black',        # Default color
            '1': 'bold',         # Bold text
            '2': 'light'         # Light text (dim)
        }

        # Regex pattern to match ANSI escape sequences
        ansi_escape = re.compile(r'\x1b\[([0-9;]+)m')

        def style_from_codes(codes):
            styles = []
            for code in codes.split(';'):
                if code in color_map:
                    color = color_map[code]
                    if color == 'bold':
                        styles.append('font-weight:bold;')
                    elif color == 'light':
                        styles.append('color:gray;')  # This could be adjusted if desired
                    else:
                        styles.append(f'color:{color};')
            return ' '.join(styles)

        # Find all ANSI escape sequences and their associated text
        parts = ansi_escape.split(log_line)
        result = []

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # This is the text between ANSI codes
                result.append(part)
            else:
                # This is the ANSI code
                codes = part.split(';')
                styles = style_from_codes(';'.join(codes))
                result.append(f'<div class="nb" style="{styles}">')

        # Join the result and wrap it in a container <div>
        html_content = ''.join(result) + '</div>'
        return f'<div>{html_content}</div>'


    def handle_request(self, client_socket, request):

        route = self.getRoute(request)
        if route == "/":
            response = self.getHomeScreen()
            self.info("Returning home screen")
        elif route == "/log":
            response = self.handleLastMessage(self.getLastMessage())
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
        setInterval(checkForUpdates, 10);
    </script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: teal;
        }
        #response {
            white-space: pre-wrap; /* Preserve whitespace and newlines */
        }

        #response div {
            display:inline;
        }
    </style>
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
