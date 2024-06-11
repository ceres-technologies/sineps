import logging

from .rest_adapter import RestAdapter, AsyncRestAdapter
from .utils import (
    validate_route_dict,
    validate_filed_dict,
)
from .intent_router import IntentRouterResponse
from .filter_extractor import FilterExtractorResponse
from .exceptions import TheSinepsApiException


class BaseClient:
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
        adapter_class=None,
    ):
        self._rest_adapter = adapter_class(
            hostname="api.sineps.io",
            api_key=api_key,
            ver=ver,
            ssl_verify=ssl_verify,
            logger=logger,
        )
        self._check_api_key()

    def _check_api_key(self):
        if not self._rest_adapter._api_key:
            raise TheSinepsApiException("SINEPS API key is required")

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        if len(routes) == 0:
            raise TheSinepsApiException("At least one route must be provided")
        for route in routes:
            validate_route_dict(route)

        data = {"query": query, "routes": routes, "allow_none": allow_none}
        return data

    def exec_filter_extractor(self, query: str, field: dict = {}):
        validate_filed_dict(field)

        data = {"query": query, "field": field}
        return data


class Client(BaseClient):
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        super().__init__(api_key, ver, ssl_verify, logger, RestAdapter)

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        data = super().exec_intent_router(query, routes, allow_none)
        result = self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    def exec_filter_extractor(self, query: str, field: dict = {}):
        data = super().exec_filter_extractor(query, field)
        result = self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)


class AsyncClient(BaseClient):
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        super().__init__(api_key, ver, ssl_verify, logger, AsyncRestAdapter)

    async def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        data = super().exec_intent_router(query, routes, allow_none)
        result = await self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    async def exec_filter_extractor(self, query: str, field: dict = {}):
        data = super().exec_filter_extractor(query, field)
        result = await self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)
