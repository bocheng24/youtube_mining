from api.youtube import YoutubeAPI
from api.settings import *
import os
import json
from api.apidata import *
from dataclasses import dataclass

class APIStarter:

    param_folder = 'general'
    param_filename = 'param.json'
    has_next_page = False

    message = 'Consume() is not suitable, try fetch()'

    def __init__(self, api_key):
        self.api_key = api_key
        self.params = self.load_params()

    @property
    def param_file_path(self):
        folder = os.path.join(PARAM_PATH, self.param_folder)
        file_path = os.path.join(folder, self.param_filename)

        return file_path

    def load_params(self):
        with open(self.param_file_path, 'r') as js:
            param_data = json.load(js)

        if 'pageToken' in param_data.key() and param_data['pageToken'] is None:
            self.has_next_page = False

        return param_data

    def save_params(self, value):
        with open(self.param_file_path, 'w') as f:
             json.dump(value, f, indent = 2)

    def fetch(self):

        yt = YoutubeAPI(self.endpoint, self.api_key, self.params)
        json_data = yt.list()

        new_data = self.DataClass(json_data)
        data.append(new_data)

        self.has_next_page = new_data.has_next_page()

        if self.has_next_page:
            new_params = {**self.params, "pageToken": new_data.nextPageToken}
            self.params = new_params

        elif not self.has_next_page and 'pageToken' in self.params.keys():
            self.params['pageToken'] = None

        self.save_params(new_params)

        return data

    def consume(self):
        all_data = []

        while self.has_next_page:
            data = self.fetch()
            all_data.append(data)

        if self.has_next_page == False and self.message:
            print(self.message)

        return all_data


class SearchAPI(APIStarter):

    endpoint = '/search'
    param_folder = 'search'
    DataClass = SearchData
    has_next_page = True
    message = 'All data have been fetched, please try another query'


    def __init__(self, api_key):
        super().__init__(api_key)


class ChannelAPI(APIStarter):
    endpoint = '/channels'
    DataClass = ChannelData

    def __init__(self, api_key, chan_id):
        super().__init__(api_key)
        self.params = {**self.load_params(), 'id': chan_id}


class PlaylistItemsAPI(APIStarter):
    endpoint = '/playlistitems'
    param_folder = 'listitems'
    DataClass = PlaylistItems
    has_next_page = True
    message = 'All uploads have been fetched'

    def __init__(self, api_key, chnl_id):
        super().__init__(api_key)
        self.chnl_id = chnl_id

    def load_params(self):
        param_data = super().load_params()
        param_data = {**param_data, 'id': self.chnl_id}

        return param_data


class VideoAPI(APIStarter):
    endpoint = '/videos'
    DataClass = VideoData
    has_next_page = False

    def __init__(self, api_key, video_id):
        super().__init__(api_key)
        self.video_id = video_id

    def load_params(self):
        param_data = super().load_params()
        param_data = {**param_data, 'id': self.video_id}

        return param_data


@dataclass
class Client:

    api_key: str
    limit_quota: int
    quota: int = 0

    def cal_quota(self, *results, typ = 'list'):

        types = {
            'list': 1
        }

        used_quota = len(results) * types[typ]
        self.quota += used_quota

    def search_wflow(self):
        print('Search workflow')

    def channels_wflow(self):
        print('Channel workflow')

    def playlistitems_wflow(self):
        print('Playlistitems_wflow workflow')

    def videos_wflow(self):
        print('Videos workflow')



