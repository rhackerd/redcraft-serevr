import inspect
from src.kons_format import consoleFormat
import datetime

last_log = {"time": datetime.datetime.now().strftime("%H:%M:%S"), "type": 0, "file": "logger.py", "text": "Not log has yet been logged."}

# 0 = info
# 1 = error
# 2 = plugin

def error(*args):
    global last_log
    filename = inspect.currentframe().f_back.f_globals['__file__'].split('/')[-1]
    time = datetime.datetime.now().strftime("%H:%M:%S")
    message = ' '.join(map(str, args))
    last_log = {"time": time, "type": 1, "file": filename, "text": message}
    print(consoleFormat(f"&<black>&d[{time}]&r &<red>&l[ERROR] &<black>&l[{filename}] &<white>{message}&r").format())

def info(*args):
    global last_log
    filename = inspect.currentframe().f_back.f_globals['__file__'].split('/')[-1]
    time = datetime.datetime.now().strftime("%H:%M:%S")
    message = ' '.join(map(str, args))
    last_log = {"time": time, "type": 0, "file": filename, "text": message}
    print(consoleFormat(f"&<black>&d[{time}]&r &<cyan>&l[INFO] &<black>&l[{filename}] &<white>{message}&r").format())

def plugin(text, plugin_name):
    global last_log
    filename = inspect.currentframe().f_back.f_globals['__file__'].split('/')[-1]
    time = datetime.datetime.now().strftime("%H:%M:%S")
    message = text
    last_log = {"time": time, "type": 2, "file": filename, "text": message}
    print(consoleFormat(f"&<black>&d[{time}]&r &<cyan>&l[INFO] &<black>&l[{filename}] &<blue>&l[{plugin_name}]&r &<magenta>&l{message}&r").format())