from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean, String, Date
Base = declarative_base()

class Input(Base):

    __tablename__ = "input_table"
    id = Column(String, primary_key=True)
    city_name = Column(String)
    destination_name = Column(String)
    date = Column (Date)
    budget = Column(Integer)

