import asyncio
import os
import requests
from dotenv import load_dotenv
from models import Input

load_dotenv()

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

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


async def main():
    state = Input(
        id="123",
        city_name="DEL",
        destination_name="RPR",
        date="2026-01-25"
    )

    api_response = await get_relevant_json(state)

    all_flights = await get_best_flights(api_response)

    print("All flight legs:\n")
    for flight in all_flights:
        print(flight)


if __name__ == "__main__":
    asyncio.run(main())
