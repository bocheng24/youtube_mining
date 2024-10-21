import requests
import pprint

class YoutubeAPI:

    base_url = 'https://www.googleapis.com/youtube/v3'

    endpoints = {
        'search': '/search',
        'videos': '/videos'
    }

    def __init__(self, endpoint, api_key, method = 'GET'):
        self.endpoint = self.endpoints[endpoint]
        self.api_key = api_key

    @property
    def url(self):
        return f'{self.base_url}{self.endpoint}?key={self.api_key}'

    def list(self, params: dict) -> None:
        params_flat = [self.url]

        for k, v in params.items():
            if isinstance(v, list):
                v = ','.join(v)

            params_flat.append(f'{k}={v}')

        full_url = '&'.join(params_flat)

        print(f'Request data following url:\n{full_url}')
        res = requests.get(full_url)

        if res.status_code == 200:
            return res.json()
        else:
            print(res)

class SearchResult:

    def __init__(self, result):
        self.prevPageToken = result.get('prevPageToken', None)
        self.nextPageToken = result.get('nextPageToken', None)
        self.regionCode = result.get('regionCode', None)

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


