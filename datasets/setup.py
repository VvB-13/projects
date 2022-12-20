from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Like(Base):
    __tablename__ = "like"

    id = Column("id", Integer, primary_key=True)
    user = Column("user", Integer)
    name = Column("name", String)
    year = Column("year", String)
    what = Column("what", String)
    players = Column("players", String)
    time = Column("playtime", Integer)
    genre = Column("genre", String)
    developer = Column("developer", String)

    def __init__(self, user, name, year, what, players, playtime, genre, developer):
        self.user = user
        self.name = name
        self.year = year
        self.what = what
        self.players = players
        self.playtime = playtime
        self.genre = genre
        self.developer = developer


engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()