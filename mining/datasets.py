from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('sqlite:///../youdb.db')

class Dataset:

    def __init__(self):
        self.search = self.load_data('search')
        self.channel = self.load_data('channel')
        self.playlistitems = self.load_data('playlistitems')
        self.video = self.load_data('video')
        self.video_tags = self.load_data('video_tags')
        self.video_detail = self.load_data('video_detail')


    def load_data(self, tablename):
        with engine.connect() as con:
            df = pd.read_sql_table(tablename, con)

        return df

def main():
    ...

if __name__ == '__main__':
    main()