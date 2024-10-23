import requests
import pprint
from datetime import datetime
import os

class YoutubeAPI:

    base_url = 'https://www.googleapis.com/youtube/v3'

    endpoints = {
        'search': '/search',
        'videos': '/videos',
        'channels': '/channels',
    }

    def __init__(self, endpoint, api_key, params):
        self.endpoint = self.endpoints[endpoint]
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
        res = requests.get(self.url)

        if res.status_code == 200:
            return res.json()
        else:
            print(res)

class SearchResult:

    def __init__(self, result):
        self.prevPageToken = result.get('prevPageToken', None)
        self.nextPageToken = result.get('nextPageToken', None)
        self.regionCode = result.get('regionCode', None)
        self.loadDatetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # a list of video Id, channel id mapping
        self.vChIdMappings = [
            {
                'videoId': item['id']['videoId'],
                'channelId': item['snippet']['channelId']
            } for item in result['items']
        ]

    def display(self):
        print(self.prevPageToken)
        print(self.nextPageToken)
        print(self.regionCode)

        for mapping in self.vChIdMappings:
            pprint.pp(mapping)

    def toDict(self):

        d = {
            'prevPageToken': self.prevPageToken,
            'nextPageToken': self.nextPageToken,
            'regionCode': self.regionCode,
            'vChIdMappings': self.vChIdMappings,
        }

        return d

    def nextPageParams(self, params):
        if self.nextPageToken:
            params['pageToken'] = self.nextPageToken
            return params

        return None

    def saveResult(self):
        result = self.toDict()
