# Sineps Python API Library

[![PyPI version](https://img.shields.io/pypi/v/sineps.svg)](https://pypi.org/project/sineps/)

The Sineps Python library provides convenient access to the Sineps REST API from any Python 3.7+ application. The library offers synchronous and asynchronous clients.

## Documentation

The REST API documentation can be found on [docs.sineps.io](https://docs.sineps.io/).

## Installation

```sh
# install from PyPI
pip install sineps
```

## Usage
### Intent Router
```python
import sineps
import os

client = sineps.Client(os.environ.get("SINEPS_API_KEY"))

query = "How do neural networks work in machine learning?"

routes = [
    {
        "name": "mathematics",
        "description": "Assign queries to this route when they are related to mathematics.",
        "utterances": [
            "What is the Pythagorean theorem?",
            "Can you explain the concept of integrals?",
            "What are the different types of symmetry in geometry?",
        ],
    },
    {
        "name": "computer_science",
        "description": "Assign queries to this route when they are related to computer science.",
        "utterances": [
            "What is the difference between Java and Python?",
            "How does deep learning work?",
            "What are the main principles of object-oriented programming?",
        ],
    },
    {
        "name": "biology",
        "description": "Assign queries to this route when they are related to biology.",
        "utterances": [
            "How do photosynthesis and cellular respiration differ?",
            "What is the structure of a DNA molecule?",
            "How do ecosystems maintain balance?",
        ],
    },
]

# Default option is to choose only a route.
res = client.exec_intent_router(query=query, routes=routes)

print(f"The chosen route: {res.result.routes[0].name}")
print(f"Index of the route: {res.result.routes[0].index}")
```
The output will be as follows:
```sh
The chosen route: computer_science
Index of the route: 1
```
### Filter Extractor
```python
import sineps
import json
import os

client = sineps.Client(os.environ.get("SINEPS_API_KEY"))

query = (
    "Find articles about the impact of Large language models on jobs and the economy, published in 2024",
)

field = {
    "name": "published_date",
    "type": "date",
    "description": "The date the article was published online.",
}

response = client.exec_filter_extractor(query=query, field=field)

print(response.result)
```
The output will be as follows:
```sh
{
 "OPERATOR": "AND",
 "VALUE": [
   {
     "OPERATOR": ">=",
     "VALUE": "2024-01-01"
   },
   {
     "OPERATOR": "<=",
     "VALUE": "2024-12-31"
   }
 ]
}
```
While you can provide an `api_key` keyword argument,
we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/)
to add `SINEPS_API_KEY="Your API Key"` to your `.env` file
so that your API Key is not stored in source control.

## Async usage

Simply use `sineps.AsyncClient` instead of `sineps.Client` and use `await` with each API call:

### Intent Router
```python
import os
import asyncio
import sineps

client = sineps.AsyncClient(os.environ.get("SINEPS_API_KEY"))

async def main() -> None:
    routes = [
        {
            "name": "mathematics",
            "description": "Assign queries to this route when they are related to mathematics.",
            "utterances": [
                "What is the Pythagorean theorem?",
                "Can you explain the concept of integrals?",
                "What are the different types of symmetry in geometry?",
            ],
        },
        {
            "name": "computer_science",
            "description": "Assign queries to this route when they are related to computer science.",
            "utterances": [
                "What is the difference between Java and Python?",
                "How does deep learning work?",
                "What are the main principles of object-oriented programming?",
            ],
        },
        {
            "name": "biology",
            "description": "Assign queries to this route when they are related to biology.",
            "utterances": [
                "How do photosynthesis and cellular respiration differ?",
                "What is the structure of a DNA molecule?",
                "How do ecosystems maintain balance?",
            ],
        },
    ]

    query = "How do neural networks work in machine learning?"
    response = await client.exec_intent_router(query=query, routes=routes)

asyncio.run(main())
```

### Filter Extractor
```python
import os
import asyncio
import sineps

client = sineps.AsyncClient(os.environ.get("SINEPS_API_KEY"))

async def main() -> None:
    query = "Find articles about the impact of Large language models on jobs and the economy, published in 2024"

    field = {
        "name": "published_date",
        "type": "date",
        "description": "The date the article was published online.",
    }
    response = await client.exec_filter_extractor(query=query, field=field)

asyncio.run(main())
```

## Handling errors

When the input format is incorrect, a subclass of `sineps.InvalidIntentRouterFormatError` is raised for the intent router, and a subclass of `sineps.InvalidFilterExtractorFormatError` is raised for the field extractor.

When the library is unable to connect to the API (for example, due to network connection problems), a subclass of `sineps.APIConnectionError` is raised.

When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of `sineps.APIStatusError` is raised, containing `status_code` and `message` properties.

All errors inherit from `sineps.APIError`.

```python
import sineps
import os

client = sineps.Client(os.environ.get("SINEPS_API_KEY"))

query = "How do neural networks work in machine learning?"

routes = [
    {
        "name": "mathematics",
        "description": "Assign queries to this route when they are related to mathematics.",
        "utterances": [
            "What is the Pythagorean theorem?",
            "Can you explain the concept of integrals?",",
        ],
    },
    {
        "name": "computer_science",
        "description": "Assign queries to this route when they are related to computer science.",
        "utterances": [
            "What is the difference between Java and Python?",
            "How does deep learning work?",
        ],
    },
]
try:
    res = client.exec_intent_router(
        query=query,
        routes=routes,
    )
except sineps.PaymentRequiredError as e:
    print("Payment required error")
    print(e.status_code)
    print(e.message)
except sineps.TooManyRequestsError as e:
    print("Too many requests error")
    print(e.status_code)
    print(e.message)


```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 401         | `UnauthorizedAPIKeyError`  |
| 402         | `PaymentRequiredError`     |
| 429         | `TooManyRequestsError`     |
| 500         | `InternalServerError`      |
| N/A         | `APIConnectionError`       |


## Requirements

Python 3.7 or higher.