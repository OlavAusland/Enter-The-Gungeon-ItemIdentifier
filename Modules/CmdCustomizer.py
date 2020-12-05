import os
import random

class Color:
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magneta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    reset = '\u001b[0m'

    @staticmethod
    def random():
        _colors = ['\u001b[31m', '\u001b[32m', '\u001b[33m',
        '\u001b[35m', '\u001b[36m']
        return random.choice(_colors)

class String:

    @staticmethod
    def set_color(string, Color):
        return f'{Color}{string}{Color.reset}'

class Window:

    @staticmethod
    def clear():
        return os.system('CLS')

    @staticmethod
    def resize(width, height):
        return os.system(f'mode con cols={width} lines={height}')

    @staticmethod
    def title(name):
        return os.system(f'title {name}')

def main():
    import os

if __name__ == '__main__':
    main()
