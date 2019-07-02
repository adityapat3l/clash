from .clan import SearchClan
from .player import SearchPlayer
import requests
import json
from . import CLASH_API_KEY
try:
    from urllib import quote  # Python2
except ImportError:
    from urllib.parse import quote  # Python 3


class BaseClashAPI:
    BASE_URL = 'https://api.clashofclans.com/v1'

    def __init__(self, path, **kwargs):
        self._path = path

        encoded_path = quote(self._path)
        self.url = self.BASE_URL + encoded_path

    def clash_request(self, params=None):
        headers = {'Authorization': 'Bearer ' + CLASH_API_KEY}
        try:
            response = requests.get(url=self.url, headers=headers, params=params)
            data = json.loads(response.content.decode('utf-8'))
            return data
        except requests.exceptions.RequestException:  # This is the correct syntax
            raise


class PlayerAPI:
    def __init__(self, **kwargs):
        self.requesting_user = None

    def get_player(self, player_tag):
        url = '/players/{}'.format(player_tag)
        data = BaseClashAPI(url).clash_request()

        return data


class ClanAPI:
    def __init__(self, **kwargs):
        self.requesting_user = None

    def get_clan(self, clan_tag):
        url = '/clans/{}'.format(clan_tag)
        data = BaseClashAPI(url).clash_request()

        return data
