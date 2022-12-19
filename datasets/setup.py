from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Likes(Base):
    __tablename__ = "likes"

    id = Column("id", Integer, primary_key=True)
    user = Column("user", Integer)
    name = Column("name", String)
    year = Column("year", Integer)
    what = Column("what", String)
    players = Column("players", String)
    playtime = Column("playtime", Integer)

    def __init__(self, user, name, year, what, players, playtime):
        self.user = user
        self.name = name
        self.year = year
        self.what = what
        self.players = players
        self.playtime = playtime

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# delete_user = session.query(Board).all()
# for user in delete_user:
#     session.delete(user)
# session.commit()

# for i in range(len(body)):
#     test = Board(name=body[i][0], year=body[i][1], min_players=body[i][2],
#             max_players=body[i][3], playtime=body[i][4])
#     session.add(test)
# session.commit()