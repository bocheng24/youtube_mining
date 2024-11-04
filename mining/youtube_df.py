import os
import pandas as pd
from datetime import datetime
import json

class YTBDF:

    def __init__(self, filenames, data_type):
        self.filenames = [filename for filename in filenames if data_type in filename]

    def get_all_json(self):

        def read_json(filename):
            datapath = '../data'
            fullpath = os.path.join(datapath, filename)
            niche = filename.split('_')[0]
            request_time = filename[: len(filename) - len('.json')].split('_')[2]
            request_time = datetime.strptime(request_time, '%m%d%Y%H%M%S')

            with open(fullpath, 'r') as js:
                data = json.load(js)

            df = pd.json_normalize(data, record_path = ['items'])

            df['niche'] = niche
            df['request_time'] = request_time

            return df

        all_dfs_lst = [read_json(filename) for filename in self.filenames]
        all_dfs = pd.concat(all_dfs_lst)

        all_dfs.columns = [col.split('.')[-1] for col in all_dfs.columns]

        all_dfs = self.clean(all_dfs)

        return all_dfs

    def clean(self, df):

        col_type_maps = {
            int: {
                    'naval': 0,
                    'values': [
                        'width', 'height', 'viewCount', 'likeCount', 'favoriteCount',
                        'commentCount', 'videoCount', 'subscriberCount'
                    ]
                }
        }

        for col in df.columns:

            for k, v in col_type_maps.items():
                if col in v['values']:
                    df[col] = df[col].fillna(v['naval'])
                    df[col] = df[col].astype(k)

        return df


