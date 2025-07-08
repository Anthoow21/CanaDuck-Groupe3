"""Tests to change a channel mode"""

import requests

SERVICE_URL = '127.0.0.1'
AUTH = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwc2V1ZG8iOiJyb2dlciIsInJvbGVzIjpbIm1vZGVyYXRvciJdLCJleHAiOjIwMDAwMDAwMDB9.E_fb6fM8MZzgP5W1B10b-GLSVJWOERo8SG9A3HgQsJk'

def scenario_one(channel: str):
    """
    Create a visible channel and change it mode. It should not be visible when calling /GET channel.
    """

    # Create a visible channel

    data = {"name": channel, "private": False}
    headers = {"authorization": AUTH}
    requests.post(f'{SERVICE_URL}/channel', json=data, headers=headers)
    
    r = requests.get(f'{SERVICE_URL}/channel')
    json_response = r.json()
    # to do : assert json_response..., check visibility in the list

    # Change the channel's mode

    data = {} # to do : see syntax
    requests.post(f'{SERVICE_URL}/channel/{channel}/mode', json=data, headers=headers)
    
    # Check the channel is invisible

    r = requests.get(f'{SERVICE_URL}/channel')
    json_response = r.json()
    # to do : assert json_response..., check it's not in the list

    requests.delete(f'{SERVICE_URL}/channel/{channel}')


if __name__ == '__main__':
    scenario_one('testMode')

