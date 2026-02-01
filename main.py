from api.youtube import YoutubeAPI
from datetime import datetime
import os
import pandas as pd

yt_api = YoutubeAPI()

params = {
    'part': 'snippet',
    'maxResults': 100,
    'videoId': '4qykb6jKXdo'
}

comments_dfs = [data.to_dataset() for data in yt_api.fetch_all_comments(params)]

df = pd.concat(comments_dfs)

df.to_csv('Output/comments.csv', index = False, sep = '\t')


