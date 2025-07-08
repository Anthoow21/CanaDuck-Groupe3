"""Tests to change a channel topic"""

import requests

SERVICE_URL = '127.0.0.1'

def scenario_one(channel: str):
    """
    Create a channel and add a topic. The topic should be updated.
    """

    # Create a channel

    data = {"name": channel, "private": False}
    requests.post(f'{SERVICE_URL}/channel', json=data)

    # Change the channel's topic

    data = {"topic": "Beleriand"}
    requests.post(f'{SERVICE_URL}/channel/{channel}/topic', json=data)
    
    # Check the topic is updated

    # to do : use GET /channel or GET/channel/testTopic/config

    # r = requests.get(f'{SERVICE_URL}/channel')
    # json_response = r.json()

    requests.delete(f'{SERVICE_URL}/channel/{channel}')


if __name__ == '__main__':
    scenario_one('testTopic')

