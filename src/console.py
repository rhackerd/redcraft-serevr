import cmd
from src.logger import info, error

class Console(cmd.Cmd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_map = {
            'test': self.test
        }
    prompt = '> '

    def do_greet(self, arg):
        'Greet the user.'
        info("Hello!")

    def test(self, arg):
        info("test")

    def do_exit(self, arg):
        'Exit the console.'
        info('Goodbye!')
        return True
    
    def help_echo(self):
        info('Echos whatever you type.')

    def do_prompt(self, arg):
        self.prompt = arg

    def do_clear(self, arg):
        print("\033[2J\033[1;1H")

    def do_plugins(self, arg):
        info("plugins:")
    
    def do_echo(self, arg):
        info(f'{arg}')
        
    def postloop(self):
        info

    def default(self, line):
        if line.strip() == '':
            return
        info(f'Unknown command: {line}')
