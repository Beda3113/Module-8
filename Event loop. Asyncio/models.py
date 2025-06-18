from sqlalchemy import Column, Integer, String, Text
from database import Base

class StarWarsPerson(Base):
    __tablename__ = 'starwars_people'

    id = Column(Integer, primary_key=True)  # ID персонажа из SWAPI
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(Text)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(Text)
    starships = Column(Text)
    vehicles = Column(Text)