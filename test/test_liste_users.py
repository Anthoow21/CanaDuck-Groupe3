"""Tests of listing channel users"""

import requests

SERVICE_URL = '127.0.0.1'
AUTH = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwc2V1ZG8iOiJyb2dlciIsInJvbGVzIjpbIm1vZGVyYXRvciJdLCJleHAiOjIwMDAwMDAwMDB9.E_fb6fM8MZzgP5W1B10b-GLSVJWOERo8SG9A3HgQsJk'

def scenario_one(channel: str):
    """
    Create a channel. It should be visible when calling /GET channel.
    """

    # Create a channel
    data = {"name": channel, "private": False}
    headers = {"authorization": AUTH}
    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)

    # List users of the channel
    r = requests.get(f'{SERVICE_URL}/channel/{channel}/users')
    json_response = r.json()
    # to do : assert users list is empty

    # Add a user in the channel
    data = {"name": "user1"}
    requests.post(f'{SERVICE_URL}/channel/{channel}/invite', json=data, headers=headers)

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
