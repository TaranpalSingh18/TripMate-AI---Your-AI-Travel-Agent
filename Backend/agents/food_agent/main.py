import asyncio
import os
import requests
from dotenv import load_dotenv
from ...models import Input
from langchain_groq import ChatGroq
from typing import List, TypedDict

class agentstate(TypedDict):
    readable_json: str
    logical_json: str

load_dotenv()

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

async def get_relevant_json(state: Input):
    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "google_flights",
        "flight_type": "round_trip",
        "departure_id": state.city_name,
        "arrival_id": state.destination_name,
        "outbound_date": state.date,
        "return_date": "2026-01-30",
        "currency": "USD",
        "api_key": SEARCH_API_KEY
    }

    response = requests.get(url, params=params)
    return response.json()

async def get_best_flights(api_response: dict) -> list:
    best_flights = api_response.get("best_flights", [])

    all_flights = []
    for flight_option in best_flights:
        all_flights.append(flight_option.get("flights", []))

    return all_flights

async def get_readable_json(all_flights: list, state: agentstate)-> dict:
    
    llm = ChatGroq(model="llama-3.1-8b-instant", api_key= groq_api_key)
    prompt = f"""
    You are a simplifier agent that converts a list having a json in it, into readable form. You are given the list as input: {all_flights}.
    Just simplify it for me and give the results
    """

    result = llm.invoke(prompt)

    return {state["readable_json"]: result.content}

async def get_logical_json(input: Input, state: agentstate)-> dict:
     
     llm = ChatGroq(model="llama-3.1-8b-instant", api_key= groq_api_key)

     prompt = f"""
You have the readable json {state["readable_json"]} and also you have my Budget: {input.budget}, Your main aim is to reason why the budget that I have is sufficient and would be worthy enough to make the trip sucessful. You have to convince me anyhow.
     """
     result = llm.invoke(prompt)

     return {state["logical_json"]: result.content}



async def main():
    state = Input(
        id="123",
        city_name="DEL",
        destination_name="RPR",
        date="2026-01-25"
    )

    api_response = await get_relevant_json(state)

    all_flights = await get_best_flights(api_response)
    print(all_flights)


if __name__ == "__main__":
    asyncio.run(main())
