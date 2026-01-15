from pydantic import BaseModel
from datetime import date
from uuid import uuid1

class Input(BaseModel):
    id: str
    city_name: str
    date: date
    budget: int

