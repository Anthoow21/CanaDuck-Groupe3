"""Channel creation tests"""

import requests

SERVICE_URL = '127.0.0.1'
AUTH = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwc2V1ZG8iOiJyb2dlciIsInJvbGVzIjpbIm1vZGVyYXRvciJdLCJleHAiOjIwMDAwMDAwMDB9.E_fb6fM8MZzgP5W1B10b-GLSVJWOERo8SG9A3HgQsJk'

def scenario_one(channel: str):
    """
    Create a channel. It should be visible when calling /GET channel.
    """

    data = {"name": channel, "private": False}
    headers = {"authorization": AUTH}

    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    assert r.status_code == 201

    json_response = r.json()
    # to do : assert json_response...

    requests.delete(f'{SERVICE_URL}/channel/{channel}')

def scenario_two(channel: str):
    """
    Create an invisible channel. It should not be visible when calling /GET channel.
    """

    data = {"name": channel, "private": True}
    headers = {"authorization": AUTH}

    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    assert r.status_code == 201

    json_response = r.json()
    # to do : assert json_response...

    requests.delete(f'{SERVICE_URL}/channel/{channel}')

def scenario_three():
    """
    Attempt to create a channel without a name.
    """

    data = {"name": "", "private": False}
    headers = {"authorization": AUTH}

    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    assert r.status_code == 400
    json_response = r.json()

    # to do : assert json_response...

def scenario_four(channel: str):
    """
    Attempt to create a channel already existing.
    """

    data = {"name": channel, "private": False}
    headers = {"authorization": AUTH}

    # Create a channel
    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)

    # Atempt to create the same channel again
    r = requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)
    assert r.status_code == 409

    requests.delete(f'{SERVICE_URL}/channel/{channel}')


if __name__ == '__main__':
    scenario_one('testCreation')
    scenario_two('testCreation')
    scenario_three()
    scenario_four('testCreation')
