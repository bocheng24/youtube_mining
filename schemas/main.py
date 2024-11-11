from .models import *
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

sr1 = Search(channel_id = 'UC75r7vrlSDBAGFfMTydsU9Q')
sr2 = Search(channel_id = 'UCYy82nDBYSbqoHQr56XP1Cg')

ch = session.query(PlaylistItems).filter_by(status = 'N').all()
print(ch)