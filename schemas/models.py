from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import create_engine

SQL_URL = 'sqlite:///youdb.db'
engine = create_engine(SQL_URL, echo = True)

class Base(DeclarativeBase):
    ...


class Search(Base):
    __tablename__ = 'search'

    channel_id: Mapped[str] = mapped_column(String(50), primary_key = True)
    status: Mapped[str] = mapped_column(String(5), default = 'N')
    load_dt: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)

    def __repr__(self):
        return f'''Search (\n\tchannel_id: {self.channel_id},\n\tload_dt: {self.load_dt}\n)'''


class Channel(Base):
    __tablename__ = 'channel'

    id: Mapped[str] = mapped_column(String(50), primary_key = True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255), default = '')
    customUrl: Mapped[str] = mapped_column(String(30))
    publishedAt: Mapped[datetime] = mapped_column(DateTime)
    uploads: Mapped[str] = mapped_column(String(50))
    viewCount: Mapped[int] = mapped_column(Integer)
    subscriberCount: Mapped[int] = mapped_column(Integer)
    videoCount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(5), default = 'N')
    load_dt: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)


class PlaylistItems(Base):
    __tablename__ = 'playlistitems'

    playlistId: Mapped[str] = mapped_column(String(50))
    videoId: Mapped[str] = mapped_column(String(50), primary_key = True)
    status: Mapped[str] = mapped_column(String(5), default = 'N')
    load_dt: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)

    def __repr__(self):
        return f'''PlaylistItems (\n\playlistId: {self.playlistId},\n\tvideoId: {self.videoId},\n\tstatus: {self.status},\n\tload_dt: {self.load_dt}\n)'''


class Video(Base):
    __tablename__ = 'video'

    id: Mapped[str] = mapped_column(String(50), primary_key = True)


Base.metadata.create_all(bind = engine)