"""Tests to change a channel mode"""

import requests

def scenario_one(channel: str):
    """
    Create a visible channel and change it mode. It should not be visible when calling /GET channel.
    """

    # Create a visible channel

    data = {"name": channel, "private": False}
    requests.post('.../channel', json=data)
    
    r = requests.get('.../channel')
    json_response = r.json()
    # to do : assert json_response..., check visibility in the list

    # Change the channel's mode

    data = {} # to do : see syntax
    requests.post(f'.../channel/{channel}/mode', json=data)
    
    # Check the channel is invisible

    r = requests.get('.../channel')
    json_response = r.json()
    # to do : assert json_response..., check it's not in the list

    requests.delete(f'.../channel/{channel}')


if __name__ == '__main__':
    scenario_one('testMode')

