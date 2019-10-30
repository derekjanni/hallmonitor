def get_auth0_token(url=None, audience=None, client_id=None, client_secret=None):
    """
    Auth0 token is required for many API calls
    """
    payload = f"audience={audience}&grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json()['access_token']
