import requests
from os import path
import json
from api.settings import PARAM_PATH, DATA_PATH


class YoutubeAPI:

    base_url = 'https://www.googleapis.com/youtube/v3'

    def __init__(self, endpoint, api_key, params):
        self.endpoint = endpoint
        self.api_key = api_key
        self.params = params

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, json_value):
        params_flat = []
        for k, v in json_value.items():
            if isinstance(v, list):
                v = ','.join(v)

            params_flat.append(f'{k}={v}')

        self._params = '&'.join(params_flat)

    @property
    def url(self):
        return f'{self.base_url}{self.endpoint}?key={self.api_key}&{self.params}'

    def list(self):
        print(f'Request data following url:\n{self.url}')

        try:
            res = requests.get(self.url)

            if res.status_code == 200:
                return res.json()
            else:
                print('Invalid response status code:')
                print(res)

        except Exception as e:
            print('Error to fetch data with following url:')
            print(self.url)
            print(e)
