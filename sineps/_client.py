import logging

from .rest_adapter import RestAdapter, AsyncRestAdapter
from .utils import (
    validate_route_dict,
    validate_filed_dict,
)
from .intent_router import IntentRouterResponse
from .filter_extractor import FilterExtractorResponse
from .exceptions import TheSinepsApiException


class Client:
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = RestAdapter(
            hostname="api.sineps.io",
            api_key=api_key,
            ver=ver,
            ssl_verify=ssl_verify,
            logger=logger,
        )

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        if len(routes) == 0:
            raise TheSinepsApiException("At least one route must be provided")
        for route in routes:
            validate_route_dict(route)

        data = {"query": query, "routes": routes, "allow_none": allow_none}
        result = self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    def exec_filter_extractor(self, query: str, field: dict = {}):
        validate_filed_dict(field)

        data = {"query": query, "field": field}
        result = self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)


class AsyncClient:
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = AsyncRestAdapter(
            hostname="api.sineps.io",
            api_key=api_key,
            ver=ver,
            ssl_verify=ssl_verify,
            logger=logger,
        )

    async def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        if len(routes) == 0:
            raise TheSinepsApiException("At least one route must be provided")
        for route in routes:
            validate_route_dict(route)

        data = {"query": query, "routes": routes, "allow_none": allow_none}
        result = await self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    async def exec_filter_extractor(self, query: str, field: dict = {}):
        validate_filed_dict(field)

        data = {"query": query, "field": field}
        result = await self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)
