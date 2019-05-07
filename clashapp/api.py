import requests
import json
from . import API_KEY
import clashapp.lib.urls as clashurl
import sys

try:
    from urllib import quote  # Python2
except ImportError:
    from urllib.parse import quote  # Python 3


class ClashAPI:
    def __init__(self):
        self.url = None

    def create_url(self, raw_url, **kwargs):
        path_value = kwargs.get('path')
        if path_value:
            # print(raw_url, path_value)
            encoded_path = quote(path_value)
            self.url = raw_url.format(path=encoded_path)
        else:
            self.url = raw_url

    def get_api_data(self, params=None):
        headers = {'Authorization': 'Bearer ' + API_KEY}
        try:
            response = requests.get(url=self.url, headers=headers, params=params)
            data = json.loads(response.content.decode('utf-8'))
            return data
        except requests.exceptions.RequestException:  # This is the correct syntax
            raise


    def get_player_info_from_tag(self, player_tag, params=None):
        self.create_url(clashurl.PLAYER_URL, path=player_tag)
        return self.get_api_data(params=params)

    def get_clan_info_from_tag(self, clan_tag, params=None):
        self.create_url(clashurl.CLAN_URL, path=clan_tag)
        return self.get_api_data(params=params)