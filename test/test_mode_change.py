"""Tests to change a channel mode"""

import requests

SERVICE_URL = '127.0.0.1'

def scenario_one(channel: str):
    """
    Create a visible channel and change it mode. It should not be visible when calling /GET channel.
    """

    # Create a visible channel

    data = {"name": channel, "private": False}
    requests.post(f'{SERVICE_URL}/channel', json=data)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    json_response = r.json()
    # to do : assert json_response..., check visibility in the list

    # Change the channel's mode

    data = {} # to do : see syntax
    requests.post(f'{SERVICE_URL}/channel/{channel}/mode', json=data)
    
    # Check the channel is invisible

    r = requests.get(f'{SERVICE_URL}/channel')
    json_response = r.json()
    # to do : assert json_response..., check it's not in the list

    requests.delete(f'{SERVICE_URL}/channel/{channel}')


if __name__ == '__main__':
    scenario_one('testMode')

