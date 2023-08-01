#!/usr/bin/env python3

'''
Copyright (c) 2023 GulagScanner
'''

from __future__ import absolute_import

import os
import sys

from .colors import G, R, W, Y, bad, end, good, tab, warn

''' try:
    from pip._internal import main as pip
except ImportError:
    print(bad + 'pip module not found...using \'ensurepip\' for solve the problem')
    subprocess.check_call([sys.executable, '-m', 'ensurepip']) '''

# enable VT100 emulation for coloR text output on windows platforms
if sys.platform.startswith('win'):
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    hStdOut = kernel32.GetStdHandle(-11)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
    mode.value |= 4
    kernel32.SetConsoleMode(hStdOut, mode)


config = {
    'http_timeout_seconds': 5,
    'response_similarity_threshold': 0.9
}

VERSION = '1.3.3.7'
DESCRIPTION = '                                 CloudFlare DNS Bypass & Analyzer'
ISSUES_PAGE = 'https://github.com/Gulag-Innovation/GulagScanner/issues/new'
GIT_REPOSITORY = 'https://github.com/Gulag-Innovation/GulagScanner.git'
GIT_PAGE = 'https://github.com/Gulag-Innovation/GulagScanner'
YEAR = '2023'
NAME = 'GulagScanner '
COPYRIGHT = 'Copyright %s - GPL v3.0' % (YEAR)
PLATFORM = os.name
IS_WIN = PLATFORM == 'nt'

answers = {
    'affirmative': ['y', 'yes', 'ok', 'okay', 'sure', 'yep', 'yeah', 'yup', 'ya', 'yeh', 'ye', 'y'],
    'negative': ['n', 'no', 'nope', 'nop', 'naw', 'na', 'nah', 'nay', 'n'],
}

# colorful banner
def logotype():
    print(Y + '''
 ██████╗ ██╗   ██╗██╗      █████╗  ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝ ██║   ██║██║     ██╔══██╗██╔════╝ ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██║  ███╗██║   ██║██║     ███████║██║  ███╗███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██║   ██║██║   ██║██║     ██╔══██║██║   ██║╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
╚██████╔╝╚██████╔╝███████╗██║  ██║╚██████╔╝███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝''' + W + '''
''' + G + DESCRIPTION + G + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + W + '\n')


BASIC_HELP = (
    'domain',
    'bruter',
    'randomAgent',
    'host',
    'outSub',
)


# osclear shortcut
def osclear():
    if IS_WIN:
        os.system('cls')
    elif 'linux' in PLATFORM:
        os.system('clear')
    else:
        print("{bad} Can't Identify Operating System!")
    logotype()
    print(Y + '\n~ Thank You For Using GulagScanner!')
    sys.exit(1)


def executer(command, **kwargs):
    try:
        if 'return' in kwargs.keys() and kwargs['return'] is True:
            return eval(command)
        exec(command)
    except Exception as e:
        if 'printError' in kwargs.keys():
            print(tab+kwargs['printError'])
            return
        print(f'{tab}{bad}{e}')


# question shortcut
def quest(question, doY='sys.exit(0)', doN='sys.exit(1)', defaultAnswerFor='yes', **kwargs):
    default = ' [Y/n]' if defaultAnswerFor.lower() in answers['affirmative'] else ' [y/N]'
    question = input(f'{question}{default}').lower().strip()

    if defaultAnswerFor.lower() == 'yes':
        answers['affirmative'].append('')
    elif defaultAnswerFor.lower() == 'no':
        answers['negative'].append('')

    if question in answers['affirmative']:
        exe = executer(doY, **kwargs)

    elif question in answers['negative']:
        exe = executer(doN, **kwargs)

    return exe


# Import Checker and downloader
class CheckImports:
    def __init__(self, libList=[]):
        for lib in libList:
            try:
                exec(lib)
            except ImportError or ModuleNotFoundError as e:
                if lib == libList[0]:
                    logotype()
                self.__downloadLib(e.name)

    def __downloadLib(self, lib):
        printMsg = {
            'printSuccess': f'{tab}{good}{lib} module is installed!',
            'printError': f'{tab}{bad}{lib} module is not installed! Try to install it manually.',
        }
        msg = f'{warn}{R}{lib}{end} Module Is Required. Do You Want To Install It?'
        command = f'subprocess.check_call([sys.executable, \'-m\', \'pip\', \'install\', \'{lib}\', '
        command += '\'--no-python-version-warning\', \'-q\', \'--disable-pip-version-check\'])'
        quest(question=msg, doY=f"import subprocess\n{command}\nprint(kwargs[\'printSuccess\'])",
              doN='continue', **printMsg)
