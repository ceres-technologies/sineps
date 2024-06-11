import sineps
import os
import asyncio
import time
import json


async def extract_field(client, query, field):
    print(f"field : {field}")
    res = await client.exec_filter_extractor(query=query, field=field)
    print(f"Field: {field['name']}")
    print(f"Filter: {json.dumps(res.filter, indent=2)}\n")


async def process_async():

    sineps_api_key = os.getenv("SINEPS_API_KEY")
    client = sineps.AsyncClient(sineps_api_key)
    query = "Search for technical books published in the last 5 years and rated over 4 stars."
    fields = [
        {
            "name": "category",
            "type": "list",
            "description": "This field refers to the genre or type of the book.",
            "values": ["technical", "fiction", "history", "science", "art", "children"],
        },
        {
            "name": "published_date",
            "type": "date",
            "description": "Date when the book was officially released.",
        },
        {
            "name": "rating",
            "type": "number",
            "description": "The average review score of the book on a scale from 1 to 5.",
        },
    ]
    start = time.time()
    await asyncio.wait(
        [
            asyncio.create_task(extract_field(client, query, fields[0])),
            asyncio.create_task(extract_field(client, query, fields[1])),
            asyncio.create_task(extract_field(client, query, fields[2])),
        ]
    )
    end = time.time()
    print(f">>> 비동기 처리 총 소요 시간: {end - start}")


if __name__ == "__main__":
    asyncio.run(process_async())
