from youtube import YoutubeAPI, SearchResult

import pprint
from os import environ
from dotenv import load_dotenv
from utils import *
from datetime import datetime


load_dotenv()
API_KEY = environ['API_KEY']

param_cfgs = {
    'search': 'valorant_shorts.json',
    'videos': 'param.json'
}

def main():
    quota = 0
    limit = 20

    while quota < limit:
        dt_postfix = datetime.now().strftime('%m%d%Y%H:%M:%S')

        outputnames = {
            'search': f'valorant_searchdata_{dt_postfix}.json',
            'videos': f'valorant_videodata_{dt_postfix}.json'
        }

        search_params = load_params('search', param_cfgs['search'])
        search_api = YoutubeAPI('search', API_KEY, search_params)
        search_data = search_api.list()

        sr = SearchResult(search_data)
        next_page_params = sr.nextPageParams(search_params)

        video_res = []

        for mapping in sr.vChIdMappings:
            params = load_params('videos', param_cfgs['videos'], id = mapping['videoId'])
            video_api = YoutubeAPI('videos', API_KEY, params)

            video_data = video_api.list()
            video_res.append(video_data)
            quota += 1

        output_json(next_page_params, param_cfgs['search'], base_folder='paramsConfigs/search')
        output_json(sr.toDict(), outputnames['search'])
        output_json(video_res, outputnames['videos'])
        quota += 1




if __name__ == '__main__':
    main()