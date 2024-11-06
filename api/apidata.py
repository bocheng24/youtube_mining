import pprint
from datetime import datetime
from schemas.models import *
from sqlalchemy.orm import sessionmaker
import isodate

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
        item = result['items'][0]
        snippet = item['snippet']
        contentDetails = item['contentDetails']
        statistics = item['statistics']

        self.id = item['id']
        self.title = snippet['title']
        self.description = snippet['description'].replace('\n', '')
        self.customUrl = snippet['customUrl']
        self.publishedAt = datetime.strptime(snippet['publishedAt'].split('T')[0], '%Y-%m-%d')
        self.uploads = contentDetails['relatedPlaylists']['uploads']
        self.viewCount = statistics['viewCount']
        self.subscriberCount = statistics['subscriberCount']
        self.videoCount = statistics['videoCount']

    def has_next_page(self):
        return False

    def saveData(self):

        exists_channel = session.query(Channel).filter_by(id = self.id).first()

        if exists_channel is None:
            new_model = Channel(
                id = self.id,
                title = self.title,
                description = self.description,
                customUrl = self.customUrl,
                publishedAt = self.publishedAt,
                uploads = self.uploads,
                viewCount = self.viewCount,
                subscriberCount = self.subscriberCount,
                videoCount = self.videoCount,
            )

            session.add(new_model)
            session.commit()

            return True

        else:
            print(f'Channel ID: {self.id} has been found in db')
            return False



class PlaylistItemsData:

    def __init__(self, result):

        self.nextPageToken = result.get('nextPageToken', None)
        self.items = result['items']

    def has_next_page(self):
        return self.nextPageToken != None

    def saveData(self):
        all_new_models = []

        for item in self.items:
            snippet = item['snippet']

            pli_model = PlaylistItems(
                playlistId = snippet['playlistId'],
                videoId = snippet['resourceId']['videoId']
            )

            exists_video = session.query(PlaylistItems).filter_by(videoId = pli_model.videoId).first()

            if exists_video is None:

                all_new_models.append(pli_model)
        print(all_new_models)
        if len(all_new_models) > 0:
            session.add_all(all_new_models)
            session.commit()
            print(f'{len(all_new_models)} new Playlist items results saved to db')

        # return True



class VideoData:
    def __init__(self, result):
        item = result['items'][0]

        snippet = item['snippet']
        statistics = item['statistics']
        contentDetails = item['contentDetails']
        topicDetails = item.get('topicDetails', {'topicCategories': ['']})

        self.id = item['id']
        self.channelId = snippet['channelId']
        self.title = snippet['title']
        self.description = snippet['description'].replace('\n', '')
        self.tags = snippet.get('tags', [''])
        self.thumbnail = snippet['thumbnails']['default']['url']
        self.publishedAt = datetime.strptime(snippet['publishedAt'].split('T')[0], '%Y-%m-%d')
        self.categoryId = snippet['categoryId']
        self.defaultLanguage = snippet.get('defaultLanguage', '')
        self.duration = isodate.parse_duration(contentDetails['duration']).total_seconds()
        self.viewCount = statistics.get('viewCount', 0)
        self.likeCount = statistics.get('likeCount', 0)
        self.commentCount = statistics.get('commentCount', 0)
        self.topicCategories = topicDetails.get('topicCategories', [''])

    def has_next_page(self):
        return False

    def saveData(self):

        exists_video = session.query(Video).filter_by(id = self.id).first()

        if exists_video is None:
            new_video = Video(
                id = self.id,
                channelId = self.channelId,
                title = self.title,
                description = self.description,
                thumbnail = self.thumbnail,
                publishedAt = self.publishedAt,
                categoryId = self.categoryId,
                defaultLanguage =self.defaultLanguage,
                duration =self.duration,
                viewCount = self.viewCount,
                likeCount = self.likeCount,
                commentCount = self.commentCount,
            )
            tag_models = [
                VideoTags(video_id = self.id, tag = tag)
                for tag in self.tags
            ]

            detail_models = [
                VideoDetail(video_id = self.id, detail_category = detail)
                for detail in self.topicCategories
            ]

            new_models = [new_video, *tag_models, *detail_models]

            session.add_all(new_models)
            session.commit()

            return True

        else:
            print(f'Channel ID: {self.id} has been found in db')
            return False
