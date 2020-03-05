import requests
import json

class Random(object):
    """
    Unclassable shits
    """

    def __init__(self):
        pass

    def get_random_joke(self):
        """
        Just uses an API to get random joke
        """
        url = 'https://icanhazdadjoke.com/'
        header = {'Accept': 'application/json'}
        joke = json.loads(requests.get(url, headers=header).text).get('joke')
        return joke
