#!/usr/bin/env python3

import yaml
import shutil
import argparse
import requests
import functools
import traceback
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
import hallmonitor.addons as addons
from colorama import Fore, Back, Style

logging.basicConfig(level=logging.DEBUG)

# Use globals to inject headers. Follow the example for Auth0 header
global AUTH_HEADER
AUTH_HEADER=None

# Define custom actions up here
def export_auth_header(header):
    global AUTH_HEADER
    AUTH_HEADER=header

ACTION_MAPPING = {
    'auth_header': export_auth_header
}

# Define custom addons here
ADDON_MAPPING = {
    'auth0': addons.auth0_handler
}

def resolve_addon(addon):
    """
    Look I know this is evil but we parse the yaml and do what it says
    to resolve addon functionality. Someday will have a better way
    """
    addon_name = addon['name']
    addon_handler = ADDON_MAPPING[addon_name]
    addon_action = addon['action']
    result = addon_handler(addon)
    action = ACTION_MAPPING[addon_action]
    action(result)


def save_response(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)


def handle_test():
    """
    Decorator for graceful connection handling
    """
    def _decorator(run_function):
        @functools.wraps(run_function)
        def _caller(*args, **kwargs):
            # Print header
            print(f'{Fore.WHITE}=' * shutil.get_terminal_size().columns)

            # Print test description
            print(f'{Fore.YELLOW}{kwargs.get("description")}')

            # Reset style
            print(Style.RESET_ALL)

            try:
                res = run_function(*args, **kwargs)
                if res.status_code == 200:
                    print(f'{Fore.BLUE}{res}')

                    if kwargs.get('json'):
                        print(f'{Fore.BLUE}{res.json()}')

                    if kwargs.get('outfile'):
                        save_response(kwargs.get('outfile'), res.content)
                else:
                    print(f'{Fore.RED}{res}')
                    print(f'{Fore.RED}{res.json()}')

                print(Style.RESET_ALL)
            except:
                print(f'{Fore.RED}')
                traceback.print_exc()
                print(Style.RESET_ALL)

        return _caller
    return _decorator


@handle_test()
def test_case(**kwargs):
    return requests.get(f'{kwargs["base"]}{kwargs["route"]}', params=kwargs.get('params'), headers=AUTH_HEADER)

def main():
    # Load optional arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", default='', help="Path to config file")
    parser.add_argument("--file", "-f", help="Name of config file", required=True)
    parser.add_argument("--cron", "-c", help="Cron expression", required=False)
    args = parser.parse_args()
    filename = args.file
    path = args.path
    cron = args.cron

    with open(f'{path}{filename}') as stream:
        config = yaml.safe_load(stream)

    addons = config.get('addons', [])
    for addon in addons:
        resolve_addon(addon)

    test_cases = config.get('test_cases', [])
    for test in test_cases:
        test_case(**test)

    if cron:
        scheduler = BlockingScheduler()
        for test in test_cases:
            job = scheduler.add_job(test_case, 'interval', kwargs=test, minutes=0.1)

        scheduler.start()

if __name__ == '__main__':
    main()
