"""Channel creation tests"""

import requests

SERVICE_URL = '127.0.0.1'

def scenario_one(channel: str):
    """
    Create a channel. It should be visible when calling /GET channel.
    """

    data = {"name": channel, "private": False}

    requests.post(f'{SERVICE_URL}/channel', json=data)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    assert r.status_code == 200

    json_response = r.json()
    # to do : assert json_response...

    requests.delete(f'{SERVICE_URL}/channel/{channel}')

def scenario_two(channel: str):
    """
    Create an invisible channel. It should not be visible when calling /GET channel.
    """

    data = {"name": channel, "private": True}

    requests.post(f'{SERVICE_URL}/channel', json=data)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    assert r.status_code == 200

    json_response = r.json()
    # to do : assert json_response...

    requests.delete(f'{SERVICE_URL}/channel/{channel}')

def scenario_three():
    """
    Attempt to create a channel without a name.
    """

    data = {"name": "", "private": False}

    requests.post(f'{SERVICE_URL}/channel', json=data)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    json_response = r.json()

    # to do : assert json_response...

if __name__ == '__main__':
    scenario_one('testCreation')
    scenario_two('testCreation')
    scenario_three()
