import requests
from os import path
import json
from api.settings import PARAM_PATH, DATA_PATH
from dotenv import dotenv_values
from schemas import api_schema

config = dotenv_values(".env")

class YoutubeAPI:

    base_url = 'https://www.googleapis.com/youtube/v3'
    api_key = config['API_KEY']

    def fetch(self, endpoint, params):

        params = {
            **params,
            'key': self.api_key
        }

        res = requests.get(f'{self.base_url}/{endpoint}', params = params)

        if res.status_code == 200:
            return res.json()

        else:
            print(res.status_code, res.text, sep=': ')

    def fetch_comments(self, params):

        endpoint = 'commentThreads'
        res_json = self.fetch(endpoint, params)

        return api_schema.CommentList(**res_json)

    def fetch_all_comments(self, params, max_iter = 5):

        nextPageToken = None
        _iter = 0

        while nextPageToken or _iter < max_iter:
            params = {**params, 'pageToken': nextPageToken}
            api_data = self.fetch_comments(params)
            nextPageToken = api_data.nextPageToken

            _iter += 1

            yield api_data



