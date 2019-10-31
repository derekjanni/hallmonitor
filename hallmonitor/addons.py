import os
import requests

def auth0_handler(auth0_config):
    token = get_auth0_token(
        url=auth0_config['url'],
        audience=auth0_config['audience'],
        grant_type=auth0_config['grant_type'],
        client_id=get_envar(auth0_config['client_id']),
        client_secret=get_envar(auth0_config['client_secret'])
    )
    return {'Authorization': f'Bearer {token}'}

def get_envar(name):
    """
    Given an envar named ${ENVAR}, look for ENVAR in the local environment and return
    """
    envar = os.environ.get(name.strip('${}'))
    if not envar:
        raise Error(f'No such environment variable to load! {name}')
    return envar

def get_auth0_token(url=None, audience=None, grant_type=None, client_id=None, client_secret=None):
    """
    Get auth0 token
    """
    payload = f"audience={audience}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(payload)
    response = requests.post(url, data=payload, headers=headers)
    return response.json()['access_token']
