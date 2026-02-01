from pydantic import BaseModel
from typing import List
from datetime import datetime

import pandas as pd

from json import load

class APIBase(BaseModel):
    kind: str
    etag: str

class VidSnippet(BaseModel):
    publishedAt: datetime
    channelId: str
    title: str
    description: str
    channelTitle: str
    tags: List[str]
    categoryId: str
    defaultLanguage: str


class VidStatistics(BaseModel):
    viewCount: int
    likeCount: int
    favoriteCount: int
    commentCount: int


class VidContDtl(BaseModel):
    '''
    Video Content Details
    '''

    duration: str
    licensedContent: bool
    projection: str


class Item(APIBase):
    kind: str
    etag: str
    id: str
    snippet: VidSnippet
    contentDetails: VidContDtl | None = None
    statistics: VidStatistics | None = None


class VideoSchema(APIBase):
    kind: str
    etag: str
    items: List[Item]

    @property
    def tags(self):
        return self.items[0].snippet.tags


class CommentSnippetB(BaseModel):
    textDisplay: str


class TLComment(APIBase):
    id: str
    snippet: CommentSnippetB


    # @property
    # def comment_text(self):
    #     return

class CommentSnippetA(BaseModel):
    channelId: str
    videoId: str
    topLevelComment: TLComment
    totalReplyCount: int


class CommentItem(APIBase):
    id: str
    snippet: CommentSnippetA

    @property
    def comment_text(self):
        return self.snippet.topLevelComment.snippet.textDisplay

    @property
    def total_reply_count(self):
        return self.snippet.totalReplyCount

    @property
    def video_id(self):
        return self.snippet.videoId

    @property
    def channel_id(self):
        return self.snippet.channelId

class CommentList(APIBase):
    nextPageToken: str | None = None
    items: List[CommentItem]


    def to_dataset(self):

        data = {
            'channel_id': [item.channel_id for item in self.items],
            'video_id': [item.video_id for item in self.items],
            'comment_text': [item.comment_text for item in self.items],
            'reply_count': [item.total_reply_count for item in self.items]
        }

        df = pd.DataFrame(data)

        return df



def main():
    with open('comments.json', 'r') as j:
        video_json = load(j)

    cmt_model = CommentList(**video_json)
    # print(cmt_model)


    with open('Output/comment_out.txt', 'w') as f:
        for item in cmt_model.items:
            f.write(f'{item.comment_text}\n')
            # print('-- ** --')


if __name__ == '__main__':
    main()