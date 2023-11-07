#File: /agent/output.py
class Output():
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
    }

    def debug(self, message):
        print(f"{self.COLORS.get('blue')}{message}{self.COLORS.get('reset')}")

    def info(self, message):
        print(f"{message}")

    def success(self, message):
        print(f"{self.COLORS.get('green')}{message}{self.COLORS.get('reset')}")

    def error(self, message):
        print(f"{self.COLORS.get('red')}{message}{self.COLORS.get('reset')}")