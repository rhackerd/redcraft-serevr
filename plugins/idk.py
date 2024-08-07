from plugins.plugin import Ex

class Plugin(Ex):
    def __init__(self):
        super().__init__("test")
        
    def onLoad(self):
        self.info("plugin is loaded")