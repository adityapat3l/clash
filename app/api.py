import requests
import json
import app.config as config
import app.lib.urls as clashurl
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
        headers = {'Authorization': 'Bearer ' + config.DEV_ADMIN_API_KEY}
        response = requests.get(
            url=self.url,
            headers=headers,
            params=params)
        # print("Currently GETing:" + response.url)
        if response.status_code == 200:
            data = json.loads(response.content.decode('utf-8'))
            return data
        else:
            raise ValueError('Clash API GET call failed with status code: ' + str(response.status_code))

    def get_player_info_from_tag(self, player_tag, params=None):
        self.create_url(clashurl.PLAYER_URL, path=player_tag)
        return self.get_api_data(params=params)

    def get_clan_info_from_tag(self, clan_tag, params=None):
        self.create_url(clashurl.CLAN_URL, path=clan_tag)
        return self.get_api_data(params=params)