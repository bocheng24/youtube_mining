from youtube import YoutubeAPI, SearchResult

import pprint
from os import environ
from dotenv import load_dotenv
from utils import *
from datetime import datetime
from sys import exit
from time import sleep, perf_counter


load_dotenv()
API_KEY = environ['API_KEY']


def main():
    limit = input('Enter quota limitation for this run:\n')

    quota = 0
    limit = int(limit)

    start = perf_counter()

    try:
        max_try = 0

        while quota < limit or max_try == 3:
            niche = 'valorant'
            dt_postfix = datetime.now().strftime('%m%d%Y%H%M%S')

            outputnames = {
                'search': f'{niche}_searchdata_{dt_postfix}.json',
                'videos': f'{niche}_videodata_{dt_postfix}.json',
                'channels': f'{niche}_channeldata_{dt_postfix}.json',
            }

            search_params = load_params('search')
            search_api = YoutubeAPI('search', API_KEY, search_params)
            search_data = search_api.list()

            sr = SearchResult(search_data)

            if sr.nextPageToken:
                next_page_params = sr.nextPageParams(search_params)
                quota += 1

                quota, video_res = consume(sr.vChIdMappings, API_KEY, 'videos', quota)
                quota, channel_res = consume(sr.vChIdMappings, API_KEY, 'channels', quota)

                output_json(next_page_params, param_type = 'search', base_folder = 'paramsConfigs/search')
                output_json(sr.toDict(), outputnames['search'])
                output_json(video_res, outputnames['videos'])
                output_json(channel_res, outputnames['channels'])

            else:
                print('Cannot find next page token, program will try again after 2 seconds')
                sleep(2)
                max_try += 1

    finally:
        end = perf_counter()
        cost_time = end - start

        cost_hr = cost_time // 3600
        cost_min = (cost_time - cost_hr * 3600) // 60
        cost_sec = (cost_time - cost_hr * 3600) % 60

        cost_str = f'{cost_hr} hr {cost_min} min {cost_sec} sec'
        print(f'Cost total {cost_str} ')
        print(f'Total quota costs: {quota}\n')

if __name__ == '__main__':
    main()