from glob import glob
from os import path
from src.logger import info, error
import importlib.util

class Mod_sys:
    def __init__(self):
        # skip plugin named plugin.py
        self.plugin_candidates = [p for p in glob("plugins/*.py") if path.basename(p) != "plugin.py"]
        self._plugins = [];
        self.plugins = []
        self.broken_plugins = []

    def check_plugin_class(self, plugin):
        module_name = path.basename(plugin)[:-3]  # remove .py extension
        spec = importlib.util.spec_from_file_location(module_name, plugin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'Plugin') and isinstance(getattr(module, 'Plugin'), type):
            return 0;
        else:
            return 1;

    def load_plugin(self, plugin):
        module_name = path.basename(plugin)[:-3]  # remove.py extension
        spec = importlib.util.spec_from_file_location(module_name, plugin)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        PluginClass = getattr(module, 'Plugin')
        plugin_instance = PluginClass()
        plugin_instance.onLoad()
        self.plugins.append(plugin_instance)
        info(f"Loaded plugin {module_name}")

    def configManager(self):
        print(self.plugins)

    def step(self):
        for i in self.plugins:
            i.step()

    def load_all_plugins(self):
        for plugin in self._plugins:
            self.load_plugin(plugin)


    def check_all_plugins(self):
        for i in self.plugin_candidates:
            if self.check_plugin_class(i) == 0:
                self._plugins.append(i)
                info(f"plugin {i} can be loaded and added to the list of plugins.")
            else:
                self.broken_plugins.append(i)
                error(f"plugin {i} doesnt have Plugin class, and cant be loaded.")


