import pprint
from datetime import datetime
from schemas.models import *
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()


class ResultData:

    def __init__(self, result):
        self.items = result['items']

    def has_next_page(self):
        return False



class SearchData:

    def __init__(self, result):
        self.prevPageToken = result.get('prevPageToken', None)
        self.nextPageToken = result.get('nextPageToken', None)
        self.regionCode = result.get('regionCode', None)
        self.loadDatetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.channelIds = set([item['snippet']['channelId'] for item in result['items']])

        # a list of video Id, channel id mapping
        # self.vChIdMappings = [
        #     {
        #         'videoId': item['id']['videoId'],
        #         'channelId': item['snippet']['channelId']
        #     } for item in result['items']
        # ]


    def has_next_page(self):
        return self.nextPageToken != None

    def display(self):
        pprint.pp(self.toDict(), indent = 2)

    def toDict(self):

        d = {
            'prevPageToken': self.prevPageToken,
            'nextPageToken': self.nextPageToken,
            'regionCode': self.regionCode,
            # 'vChIdMappings': self.vChIdMappings,
            'channelIds': self.channelIds,
            'loadDatetime': self.loadDatetime
        }

        return d

    def saveData(self):
        new_models = []
        for channel_id in self.channelIds:
            sr = session.query(Search).filter_by(channel_id = channel_id).first()

            if sr is None:
                new_models.append(Search(channel_id = channel_id))

        if len(new_models) > 0:
            session.add_all(new_models)
            session.commit()
            print(f'{len(new_models)} new Search results saved to db')

        else:
            print('No new search results found')


class ChannelData:
    def __init__(self, result):
        snippet = result['snippet']
        contentDetails = result['contentDetails']

        self.id = result['id']
        self.title = snippet['title']
        self.description = snippet['description']
        self.customUrl = snippet['customUrl']
        self.publishedAt = datetime.strptime(snippet['publishedAt'].split('T')[0], '%Y-%m-%d')
        self.uploads = contentDetails['uploads']

    def saveData(self):

        exists_channel = session.query(Channel).filter_by(id = self.id).first()

        if exists_channel is None:
            new_model = Channel(self.id, self.title, self.description, self.customUrl, self.publishedAt, self.uploads)

            session.add(new_model)
            session.commit()

        else:
            print(f'Channel ID: {self.id} has been found in db')



class PlaylistItemsData:

    def __init__(self, result):

        self.channel_id = result['snippet']


class VideoData:
    ...
