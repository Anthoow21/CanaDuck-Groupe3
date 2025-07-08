"""Tests to ban a user"""

import requests

SERVICE_URL = '127.0.0.1'

def scenario_one(channel: str):
    """
    Create a channel and ban someone who have join.
    """

    # Create a channel

    data = {"name": channel, "private": False}
    requests.post(f'{SERVICE_URL}/channel', json=data)

    # Invite the user

    data = {"name": "Beleriand", } 
    requests.post(f'{SERVICE_URL}/channel/{channel}/invite', json=data)
    
    # Check if the user has join the channel
    
    requests.get(f'{SERVICE_URL}/channel/{channel}/users')
    
    # Ban the user

    data = {"name": "Beleriand", } 
    requests.post(f'{SERVICE_URL}/channel/{channel}/ban', json=data)

    # Check the topic is updated

    # to do : use GET /channel or GET/channel/testTopic/config

    # r = requests.get(f'{SERVICE_URL}/channel')
    # json_response = r.json()

    #Delete the test :

    requests.delete(f'{SERVICE_URL}/channel/{channel}')


if __name__ == '__main__':
    scenario_one('testTopic')