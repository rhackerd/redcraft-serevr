import pygame
import threading
import queue
from plugins.plugin import Ex

class Plugin(Ex):
    def __init__(self):
        super().__init__("gui")
        self.generateFolder()
        self.generateConfig()
        
        # Queue for inter-thread communication
        self.command_queue = queue.Queue()
        
        # Start the Pygame thread
        self.thread = threading.Thread(target=self.run_pygame)
        self.thread.start()

    def run_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygame GUI")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Process commands from other threads
            while not self.command_queue.empty():
                command = self.command_queue.get()
                # Handle the command
                if command == "quit":
                    running = False

            # Clear the screen with black
            self.screen.fill((0, 0, 0))
            
            # Update the display
            pygame.display.flip()

        pygame.quit()

    def step(self):
        # This method can be called from other threads
        self.command_queue.put("some_command")
    
    def stop(self):
        self.command_queue.put("quit")
        self.thread.join()

# Usage
plugin = Plugin()
plugin.step()
# To stop the Pygame thread cleanly
plugin.stop()
