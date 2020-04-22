#!/usr/bin/env python3

import yaml
import shutil
import argparse
import requests
import functools
import traceback
import logging
from pprint import pprint
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import hallmonitor.services.endpoint as endpoint_service
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
                        pprint(f'{Fore.BLUE}{res.json()}')

                    if kwargs.get('outfile'):
                        save_response(kwargs.get('outfile'), res.content)
                else:
                    print(f'{Fore.RED}{res}')
                    pprint(f'{Fore.RED}{res.json()}')

                print(Style.RESET_ALL)
                if kwargs.get('store_results'):
                    endpoint_service.store_results(kwargs, res)

            except:
                print(f'{Fore.RED}')
                traceback.print_exc()
                print(Style.RESET_ALL)

        return _caller
    return _decorator


@handle_test()
def test_case(**kwargs):
    method = kwargs.get('method')
    method_mapping = {
        'GET': functools.partial(requests.get),
        'PUT': functools.partial(requests.put),
        'POST': functools.partial(requests.post),
        'DELETE': functools.partial(requests.delete),
    }
    request_function = method_mapping.get(method)
    if not request_function:
        raise Exception(f'{method} is not a valid HTTP request method! Try something from {method_mapping}')

    return request_function(f'{kwargs["base"]}{kwargs["route"]}', params=kwargs.get('params'), headers=AUTH_HEADER, data=kwargs.get('data'))

def main(config=None, cli=True, **kwargs):
    print(f'config {config}')
    print(f'cli {cli}')
    print(f'kwargs {kwargs}')
    if cli is True:
        # Load optional arguments if using cli. Otherwise pass args from main
        parser = argparse.ArgumentParser()
        parser.add_argument("--path", "-p", default='', help="Path to config file")
        parser.add_argument("--file", "-f", help="Name of config file", required=True)
        parser.add_argument("--name", "-n", help="Name of test to run in --file", default=None)
        parser.add_argument("--monitor", "-m", help="Turns on monitoring", action='store_true')
        parser.add_argument("--schedule", "-s", help="Minute schedule to run this on", type=float, default=0.1)
        args = parser.parse_args()
        filename = args.file
        test_name = args.name
        path = args.path
        monitor = args.monitor
        schedule = args.schedule
        scheduler = BackgroundScheduler()
    else:
        monitor = kwargs.get('monitor')
        schedule = kwargs.get('schedule', 0.1)
        scheduler = BackgroundScheduler()
        test_name = None

    if not config:
        with open(f'{path}{filename}') as stream:
            config = yaml.safe_load(stream)

    addons = config.get('addons', [])
    for addon in addons:
        resolve_addon(addon)

    test_cases = config.get('test_cases', [])
    if test_name:
        for test in test_cases:
            if test_name == test.get('name', 'No Name'):
                test_case(**test)
    else:
        for test in test_cases:
            test_case(**test)

    if monitor:
        for test in test_cases:
            test['store_results'] = True
            job = scheduler.add_job(test_case, 'interval', kwargs=test, minutes=schedule)

        scheduler.start()

if __name__ == '__main__':
    main()
