from plugins.plugin import Ex

class Plugin(Ex):
    def __init__(self):
        super().__init__("testing")
        self.createGameCommand(lambda: print("hello from console"), ["test"], "test")
        
    def onLoad(self):
        super().info("plugin is loaded")

    def onUnload(self):
        super().info("plugin is unloaded")

