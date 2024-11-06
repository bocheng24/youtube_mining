from api.youtube import YoutubeAPI
from api.settings import *
import os
import json
from api.apidata import *
from dataclasses import dataclass
from colorama import Fore
from time import sleep

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

    def load_params(self, **kwargs):
        with open(self.param_file_path, 'r') as js:
            param_data = json.load(js)

        if 'pageToken' in param_data.keys() and param_data['pageToken'] is None:
            del param_data['pageToken']

        return param_data

    def save_params(self, value):
        with open(self.param_file_path, 'w') as f:
             json.dump(value, f, indent = 2)

    def fetch(self):

        yt = YoutubeAPI(self.endpoint, self.api_key, self.params)
        json_data = yt.list()

        new_data = self.DataClass(json_data)
        # data.append(new_data)

        self.has_next_page = new_data.has_next_page()

        if self.has_next_page:
            new_params = {**self.params, "pageToken": new_data.nextPageToken}
            self.params = new_params

        elif not self.has_next_page and 'pageToken' in self.params.keys():
            self.params['pageToken'] = None

        self.save_params(self.params)

        return new_data

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
    endpoint = '/playlistItems'
    param_folder = 'listitems'
    DataClass = PlaylistItemsData
    has_next_page = True
    message = 'All playlist uploads have been fetched'

    def __init__(self, api_key, playlistId):
        super().__init__(api_key)
        self.playlistId = playlistId
        self.params = {**self.load_params(), 'playlistId': playlistId}



class VideoAPI(APIStarter):
    endpoint = '/videos'
    DataClass = VideoData
    has_next_page = False

    def __init__(self, api_key, video_id):
        super().__init__(api_key)
        self.params = {**self.load_params(), 'id': video_id}


@dataclass
class Client:

    api_key: str
    limit_quota: int = 100
    quota: int = 0

    def cal_quota(self, *results, typ = 'list'):

        types = {
            'list': 1
        }

        used_quota = len(results) * types[typ]
        self.quota += used_quota

    def search_wflow(self):

        try:
            while self.quota <= self.limit_quota:
                self.playlistitems_query()
                self.video_query()
                self.search_query()
                self.channel_query()

                print(f'{Fore.MAGENTA}***** Waiting for 2 seconds')
                sleep(2)
                print(f'{Fore.GREEN}Time is up *****{Fore.RESET}')

        except Exception as e:
            print(e)

        finally:
            print(self.quota)
            # running = self.quota < self.limit_quota

    def search_query(self):

        exists_search = session.query(Search).filter_by(status = 'N').first()

        if exists_search is None:
            search_api = SearchAPI(self.api_key)

            search_data = search_api.fetch()
            self.cal_quota()
            search_data.saveData()
            print('quota', self.quota)

        print(f'>>>>>>>>>>>> {Fore.GREEN}Fetched all search items of this page{Fore.RESET}')

    def channel_query(self):

        new_channel = session.query(Search).filter_by(status = 'N').first()

        while new_channel:
            chnl_api = ChannelAPI(self.api_key, new_channel.channel_id)
            chnl_data = chnl_api.fetch()
            self.cal_quota(chnl_data)

            saved = chnl_data.saveData()

            if saved:
                new_channel.status = 'Y'
                session.commit()

                new_channel = session.query(Search).filter_by(status = 'N').first()

            else:
                print(f'{Fore.RED}Something with saving the new channel{Fore.RESET}')

        print(f'>>>>>>>>>>>> {Fore.GREEN}Fetched all Channels{Fore.RESET}')

    def playlistitems_query(self):
        new_upload = session.query(Channel).filter_by(status = 'N').first()

        while new_upload:

            pli_api = PlaylistItemsAPI(self.api_key, new_upload.uploads)
            pli_data = pli_api.consume()
            self.cal_quota(*pli_data)

            for pli in pli_data:
                pli.saveData()

            new_upload.status = 'Y'
            session.commit()

            new_upload = session.query(Channel).filter_by(status = 'N').first()

        print(f'>>>>>>>>>>>> {Fore.GREEN}Fetched all playlist items{Fore.RESET}')

    def video_query(self):

        new_video = session.query(PlaylistItems).filter_by(status = 'N').first()

        while new_video:
            video_api = VideoAPI(self.api_key, new_video.videoId)
            video_data = video_api.fetch()
            self.cal_quota(video_data)

            saved = video_data.saveData()

            if saved:
                new_video.status = 'Y'
                session.commit()

            new_video = session.query(PlaylistItems).filter_by(status = 'N').first()

        print(f'>>>>>>>>>>>> {Fore.GREEN}Fetched all videos{Fore.RESET}')








