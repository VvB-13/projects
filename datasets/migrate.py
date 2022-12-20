import csv
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reading CSV into Memory with header and body
body = []
with open("steam_games.csv", "r") as file:
    reader = csv.reader(file, delimiter = ";")
    header = next(reader)
    for row in reader:
        body.append(row)

for i in range(len(body)):
    for y in range(21, 18, -1):
        body[i].pop(y)
    for y in range(17, 5, -1):
        body[i].pop(y)
    body[i].pop(4)
    body[i].pop(2)
    body[i].pop(0)

Base = declarative_base()

class Game(Base):
    __tablename__ = "game"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    release = Column("release", String)
    genre = Column("genre", String)
    developer = Column("runtime", String)

    def __init__(self, title, release, genre, developer):
        self.title = title
        self.release = release
        self.genre = genre
        self.developer = developer

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

for i in range(len(body)):
    test = Game(title=body[i][0], developer=body[i][1], genre=body[i][2], release=body[i][3])
    session.add(test)
session.commit()