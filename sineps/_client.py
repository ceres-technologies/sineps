import logging
import json

from .rest_adapter import RestAdapter
from .utils import add_index_to_dictionary_list, uppercase_keys
from .intent_router import IntentRouterResponse
from .filter_extractor import FilterExtractorResponse


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
        routes = add_index_to_dictionary_list(routes)
        if allow_none:
            option = "single_none"
        else:
            option = "single"
        data = {"query": query, "routes": routes, "option": option}
        result = self._rest_adapter.post("/intent-router", data=data)
        return IntentRouterResponse(result, routes)

    def exec_filter_extractor(self, query: str, field: dict = {}):
        field = uppercase_keys(field)
        field_str = json.dumps(field)
        data = {"natural_language_query": query, "metadata_schema": field_str}
        result = self._rest_adapter.post("/filter-extractor", data=data)
        return FilterExtractorResponse(result)
