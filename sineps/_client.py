import logging

from ._rest_adapter import RestAdapter, AsyncRestAdapter
from ._validate import validate_intent_router_format, validate_filter_extractor_format
from .intent_router import IntentRouterResponse
from .filter_extractor import FilterExtractorResponse
from ._exceptions import (
    SinepsException,
    SinepsClientException,
    SinepsAsyncClientException,
)


class BaseClient:
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
        adapter_class=None,
        exception_class=None,
    ):
        self._rest_adapter = adapter_class(
            hostname="api.sineps.io",
            api_key=api_key,
            ver=ver,
            ssl_verify=ssl_verify,
            logger=logger,
            exception_class=exception_class,
        )
        self._check_api_key()

    def _check_api_key(self):
        if not self._rest_adapter._api_key:
            raise SinepsException("SINEPS API key is required")

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        # validate_intent_router_format(query, routes, allow_none)
        data = {"query": query, "routes": routes, "allow_none": allow_none}
        return data

    def exec_filter_extractor(
        self, query: str, field: dict = {}, required: bool = False
    ):
        validate_filter_extractor_format(query, field, required)
        data = {"query": query, "field": field, "required": required}
        return data


class Client(BaseClient):
    def __init__(
        self,
        api_key: str = "",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        super().__init__(
            api_key,
            ver,
            ssl_verify,
            logger,
            RestAdapter,
            exception_class=SinepsClientException,
        )

    def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        data = super().exec_intent_router(query, routes, allow_none)
        result = self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    def exec_filter_extractor(
        self, query: str, field: dict = {}, required: bool = False
    ):
        data = super().exec_filter_extractor(query, field, required)
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
        super().__init__(
            api_key,
            ver,
            ssl_verify,
            logger,
            AsyncRestAdapter,
            exception_class=SinepsAsyncClientException,
        )

    async def exec_intent_router(
        self, query: str, routes: list = [], allow_none: bool = False
    ):
        data = super().exec_intent_router(query, routes, allow_none)
        result = await self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    async def exec_filter_extractor(
        self, query: str, field: dict = {}, required: bool = False
    ):
        data = super().exec_filter_extractor(query, field, required)
        result = await self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)
