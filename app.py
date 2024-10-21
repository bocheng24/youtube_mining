from youtube import YoutubeAPI, SearchResult

import pprint
import json
from os import path, environ
from dotenv import load_dotenv

load_dotenv()
API_KEY = environ['API_KEY']

def load_params(endpoint, json_file, **kwargs):
    base = 'paramsConfigs'
    sub_foloder = path.join(base, endpoint)
    json_path = path.join(sub_foloder, json_file)

    with open(json_path, 'r') as js:
        data = json.load(js)

    if kwargs:
        data = {**data, **kwargs}

    return data



def main():
    search_api = YoutubeAPI('search', API_KEY)
    search_data = search_api.list(load_params('search', 'valorant_shorts.json'))

    sr = SearchResult(search_data)

    for mapping in sr.vChIdMappings:
        video_api = YoutubeAPI('videos', API_KEY)
        params = load_params('videos', 'param.json', id = mapping['videoId'])

        video_data = video_api.list(params)
        pprint.pp(video_data)



if __name__ == '__main__':
    main()