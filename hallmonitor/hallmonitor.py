#!/usr/bin/env python

import yaml
import shutil
import argparse
import requests
import functools
import logging
from colorama import Fore, Back, Style

logging.basicConfig(level=logging.DEBUG)

def handle_test():
    """
    Decorator for graceful connection handling
    """
    def _decorator(run_function):
        @functools.wraps(run_function)
        def _caller(*args, **kwargs):
            # Check for cached response.
            print(f'{Fore.WHITE}=' * shutil.get_terminal_size().columns)
            print(f'{Fore.YELLOW}{kwargs.get("description")}')
            print(Style.RESET_ALL)
            res = run_function(*args, **kwargs)
            if res.status_code == 200:
                print(f'{Fore.BLUE}{res}')
                if kwargs.get('json'):
                    print(f'{Fore.BLUE}{res.json()}')

            else:
                print(f'{Fore.RED}{res}')
                print(f'{Fore.RED}{res.json()}')

            print(Style.RESET_ALL)
            return res

        return _caller
    return _decorator

@handle_test()
def test_case(auth=None, **kwargs):
    return requests.get(f'{kwargs["base"]}{kwargs["url"]}', params=kwargs.get('params'), headers=auth)

if __name__ == '__main__':
    # Load optional arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--file", "-f", help="name of config file")
    args = parser.parse_args()
    filename = args.file

    with open(f'{filename}') as stream:
        config = yaml.safe_load(stream)

    test_cases = config['test_cases']
    for test in test_cases:
        test_case(**test)
