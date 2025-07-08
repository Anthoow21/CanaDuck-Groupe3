"""Tests of listing channel users"""

import requests

SERVICE_URL = '127.0.0.1'

def scenario_one(channel: str):
    """
    Create a channel. It should be visible when calling /GET channel.
    """

    # Create a channel
    data = {"name": channel, "private": False}
    requests.post(f'{SERVICE_URL}/channel', json=data)

    # List users of the channel
    r = requests.get(f'{SERVICE_URL}/channel/{channel}/users')
    json_response = r.json()
    # to do : assert users list is empty

    # Add a user in the channel
    data = {"name": "user1"}
    requests.post(f'{SERVICE_URL}/channel/{channel}/invite', json=data)

    # List users of the channel
    r = requests.get(f'{SERVICE_URL}/channel/{channel}/users')
    json_response = r.json()
    # to do : assert user1 is in the list

    requests.delete(f'{SERVICE_URL}/channel/{channel}')

def scenario_two(channel: str):
    """
    It shouldn't be possible to list users from a non-existing channel.
    """

    r = requests.get(f'{SERVICE_URL}/channel/{channel}/users')
    json_response = r.json()

    # to do : assert return code and json error

if __name__ == '__main__':
    scenario_one('testUserList')
    scenario_two('unknownUserListChannel')
