import os

def blank_line():
    print('')

def bold(text):
    return '\033[1m' + text + '\033[0m'

def bold_italic(text):
    return '\033[3m\033[1m' + text + '\033[0m'

def bold_underline(text):
    return '\033[4m\033[1m' + text + '\033[0m'

def bold_underline_italic(text):
    return '\033[3m\033[4m\033[1m' + text + '\033[0m'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color):
    color_codes = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'grey': '\033[90m',
        'dark_grey': '\033[2m',
        'dark_blue': '\033[34m\033[2m',
        'light_blue': '\033[94m',
        'dark_green': '\033[32m\033[2m',
        'light_green': '\033[92m',
        'dark_red': '\033[31m\033[2m',
        'light_red': '\033[91m',
        'pink': '\033[95m',
        'orange': '\033[33m\033[91m',
        'reset': '\033[0m'
    }
    if color.startswith('#'):
        r, g, b = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        color_code = f'\033[38;2;{r};{g};{b}m'
    elif ',' in color:
        r, g, b = color.split(',')
        color_code = f'\033[38;2;{r};{g};{b}m'
    else:
        color_code = color_codes.get(color.lower(), color_codes['reset'])
    return f'{color_code}{text}\033[0m'

def italic(text):
    return '\033[3m' + text + '\033[0m'

def strikethrough(text):
    return '\033[9m' + text + '\033[0m'

def underline(text):
    return '\033[4m' + text + '\033[0m'

def underline_italic(text):
    return '\033[3m\033[4m' + text + '\033[0m'

def yes_or_no(boolean):
    if boolean:
        return 'Yes'
    else:
        return 'No '