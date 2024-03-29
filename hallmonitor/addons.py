import os
import requests
from keycloak import KeycloakOpenID

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
    return os.environ.get(name.strip('${}'))

def get_auth0_token(url=None, audience=None, grant_type=None, client_id=None, client_secret=None):
    """
    Get auth0 token
    """
    payload = f"audience={audience}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    print(payload)
    response = requests.post(url, data=payload, headers=headers)
    return response.json()['access_token']

def keycloak_handler(keycloak_config):
    """
    Keycloak token is required for many API calls
    """
    # Configure client
    if keycloak_config.get('client_secret'):
        keycloak_openid = KeycloakOpenID(
            server_url=keycloak_config['url'],
            client_id=get_envar(keycloak_config['client_id']),
            realm_name=keycloak_config['realm'],
            client_secret_key=get_envar(keycloak_config['client_secret'])
        )
    else:
        keycloak_openid = KeycloakOpenID(
            server_url=keycloak_config['url'],
            client_id=get_envar(keycloak_config['client_id']),
            realm_name=keycloak_config['realm'],
            client_secret_key=get_envar(keycloak_config['client_secret'])
        )
    # Get Token
    token = keycloak_openid.token(get_envar(keycloak_config['user']), get_envar(keycloak_config['password']))
    token = token['access_token']
    return {'Authorization': f'Bearer {token}'}
