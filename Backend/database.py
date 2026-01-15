from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine= create_engine("postgresql://postgres:taran1234@localhost:5432/makemedrip")

session = sessionmaker(bind=engine)