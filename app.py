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

def output_json(data, file_name):
    base = 'data'
    with open(path.join(base, file_name), 'w') as output:
        json.dump(data, output, indent=2)

def main():
    search_api = YoutubeAPI('search', API_KEY)
    search_data = search_api.list(load_params('search', 'valorant_shorts.json'))

    sr = SearchResult(search_data)

    video_res = []

    for mapping in sr.vChIdMappings:
        video_api = YoutubeAPI('videos', API_KEY)
        params = load_params('videos', 'param.json', id = mapping['videoId'])

        video_data = video_api.list(params)
        video_res.append(video_data)

    output_json(video_res, 'result_valorant_shorts.json')



if __name__ == '__main__':
    main()