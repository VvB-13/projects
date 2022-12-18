import csv
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Reading CSV into Memory with header and body
body = []
with open("bgg.csv", "r") as file:
    reader = csv.reader(file, delimiter = ";")
    header = next(reader)
    for row in reader:
        body.append(row)

for i in range(len(body)):
    body[i].pop(13)
    body[i].pop(12)
    body[i].pop(11)
    body[i].pop(10)
    body[i].pop(9)
    body[i].pop(8)
    body[i].pop(7)
    body[i].pop(0)

Base = declarative_base()

class Board(Base):
    __tablename__ = "board"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    year = Column("year", Integer)
    min_players = Column("min_players", Integer)
    max_players = Column("max_players", Integer)
    playtime = Column("playtime", Integer)

    def __init__(self, name, year, min_players, max_players, playtime):
        self.name = name
        self.year = year
        self.min_players = min_players
        self.max_players = max_players
        self.playtime = playtime

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# delete_user = session.query(Board).all()
# for user in delete_user:
#     session.delete(user)
# session.commit()

for i in range(len(body)):
    test = Board(name=body[i][0], year=body[i][1], min_players=body[i][2],
            max_players=body[i][3], playtime=body[i][4])
    session.add(test)

session.commit()