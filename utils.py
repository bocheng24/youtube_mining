from os import path
import json
from youtube import YoutubeAPI


def get_param_path(param_type):

    param_cfgs = {
        'base': 'paramsConfigs',
        'search': 'valorant_shorts.json',
        'general': 'param.json'
    }

    subfolder = path.join(param_cfgs['base'], param_type)
    param_path = path.join(subfolder, param_cfgs[param_type])

    return param_path

def load_params(param_type, **kwargs):

    param_path = get_param_path(param_type)

    with open(param_path, 'r') as js:
        data = json.load(js)

    if kwargs:
        data = {**data, **kwargs}

    return data

def output_json(data, file_name = None, param_type = None, base_folder = 'data'):

    if param_type:
        full_path = get_param_path(param_type)

    else:
        full_path = path.join(base_folder, file_name)

    with open(full_path, 'w') as output:
        json.dump(data, output, indent=2)

def consume(all_data, API_KEY, endpoint, quota, param_type = 'general'):

    id_types = {
        'videos': 'videoId',
        'channels': 'channelId',
    }

    results = []

    for data in all_data:
        params = load_params(param_type, id = data[id_types[endpoint]])
        video_api = YoutubeAPI(endpoint, API_KEY, params)

        result_data = video_api.list()
        results.append(result_data)
        quota += 1

    return quota, results
