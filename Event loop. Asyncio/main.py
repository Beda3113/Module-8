import asyncio
import aiohttp
from models import StarWarsPerson
from database import AsyncSessionLocal
from sqlalchemy.exc import IntegrityError
from tqdm.asyncio import tqdm

SWAPI_URL = "https://swapi.dev/api/people/" 

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_related_names(session, urls):
    if not urls:
        return ""
    names = []
    for url in urls:
        try:
            data = await fetch_data(session, url)
            names.append(data.get("name"))
        except Exception as e:
            print(f"Ошибка при получении имени по URL {url}: {e}")
    return ", ".join(filter(None, names))

async def fetch_person(session, person_data):
    async with AsyncSessionLocal() as db_session:
        try:
            person_id = int(person_data["url"].split("/")[-2])

            films = await get_related_names(session, person_data["films"])
            species = await get_related_names(session, person_data["species"])
            starships = await get_related_names(session, person_data["starships"])
            vehicles = await get_related_names(session, person_data["vehicles"])

            homeworld_name = ""
            if person_data["homeworld"]:
                homeworld_data = await fetch_data(session, person_data["homeworld"])
                homeworld_name = homeworld_data.get("name", "")

            person = StarWarsPerson(
                id=person_id,
                birth_year=person_data["birth_year"],
                eye_color=person_data["eye_color"],
                films=films,
                gender=person_data["gender"],
                hair_color=person_data["hair_color"],
                height=person_data["height"],
                homeworld=homeworld_name,
                mass=person_data["mass"],
                name=person_data["name"],
                skin_color=person_data["skin_color"],
                species=species,
                starships=starships,
                vehicles=vehicles,
            )

            db_session.add(person)
            await db_session.commit()
        except IntegrityError:
            await db_session.rollback()
        except Exception as e:
            print(f"Ошибка при обработке {person_data['url']}: {e}")
            await db_session.rollback()

async def fetch_all_people():
    async with aiohttp.ClientSession() as session:
        next_url = SWAPI_URL
        people_to_process = []

        # Сначала собираем всех персонажей, чтобы знать общее количество
        while next_url:
            data = await fetch_data(session, next_url)
            people_to_process.extend(data["results"])
            next_url = data["next"]

        # Прогресс-бар
        tasks = [fetch_person(session, person) for person in people_to_process]
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Загрузка персонажей"):
            await task

if __name__ == "__main__":
    asyncio.run(fetch_all_people())