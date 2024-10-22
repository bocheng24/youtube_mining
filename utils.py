from os import path
import json

def load_params(endpoint, json_file, **kwargs):
    base = 'paramsConfigs'
    sub_folder = path.join(base, endpoint)
    json_path = path.join(sub_folder, json_file)

    with open(json_path, 'r') as js:
        data = json.load(js)

    if kwargs:
        data = {**data, **kwargs}

    return data

def output_json(data, file_name, base_folder = 'data'):

    with open(path.join(base_folder, file_name), 'w') as output:
        json.dump(data, output, indent=2)