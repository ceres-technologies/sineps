import sineps
import os
import asyncio
import time


async def find_route(client, query, routes):
    print(f"query : {query}")
    res = await client.exec_intent_router(query=query, routes=routes)
    print(f"The chosen route: {res.chosen.routes[0].name}")
    print(f"Index of the route: {res.chosen.routes[0].index}")


async def process_async():

    sineps_api_key = os.getenv("SINEPS_API_KEY")
    client = sineps.AsyncClient(sineps_api_key)

    routes = [
        {
            "name": "Physics",
            "description": "This route is for query which asks about concepts in physics",
            "utterances": [
                "I want to know about Newton's Laws of Motion",
                "Explain me about superstring theory",
                "Why the earth is rotating?",
            ],
        },
        {
            "name": "Math",
            "description": "This route is for query which asks about concepts in math",
            "utterances": ["1+1=?", "What is the derivative of e^-x?"],
        },
        {
            "name": "Computer science",
            "description": "This route is for query which asks about concepts in computer science",
            "utterances": [
                "How can I learn python programming language?",
                "What is the best IDE for Go?",
            ],
        },
    ]

    queries = [
        "What is a black hole?",
        "What is the derivative of x^2?",
        "How can I learn python programming language?",
    ]
    start = time.time()
    await asyncio.wait(
        [
            asyncio.create_task(find_route(client, queries[0], routes)),
            asyncio.create_task(find_route(client, queries[1], routes)),
            asyncio.create_task(find_route(client, queries[2], routes)),
        ]
    )
    end = time.time()
    print(f">>> 비동기 처리 총 소요 시간: {end - start}")


if __name__ == "__main__":
    asyncio.run(process_async())
