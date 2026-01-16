from fastapi import FastAPI
from validator import Input
from database import session, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

inputs = [Input(id="128", city_name="Delhi", date="2026-08-10", budget=10000)]

def init_db ():
    db = session()

    for input in inputs:
        db.add(models.Input(**input.model_dump()))

    db.commit ()

init_db()


@app.get('/view-all')
async def view_all_inputs():
    db = session()
    db.query()


@app.post('/input')
async def input_params(data: Input):
    return {
        "id": data.id,
        "city": data.city_name,
        "destination name": data.destination_name,
        "date": data.date,
        "budget": data.budget
    }