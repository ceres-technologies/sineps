import json
from typing import List

from ._rest_adapter import Response


INDENT = 2


class Route:
    def __init__(
        self,
        name: str,
        description: str,
        utterances=[],
        index=None,
    ):
        self.index = index
        self.name = name
        self.description = description
        self.utterances = utterances

    def to_str_dict(self):
        if self.index is None:
            return {
                "name": self.name,
                "description": self.description,
                "utterances": self.utterances,
            }
        else:
            return {
                "index": self.index,
                "name": self.name,
                "description": self.description,
                "utterances": self.utterances,
            }

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "utterances": self.utterances,
        }

    def __repr__(self, indent=INDENT):
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self, indent=INDENT):
        return json.dumps(self.to_str_dict(), indent=indent)


class Routes:
    def __init__(self, routes: List[Route]):
        self.routes = routes

    def to_dict(self):
        return [route.to_dict() for route in self.routes]

    def __repr__(self, indent=INDENT):
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self, indent=INDENT):
        return json.dumps(self.to_dict(), indent=indent)


class IntentRouterResponse:
    def __init__(self, response: Response, all_routes: List[dict]):
        self.result = self._get_result(response.data, all_routes)

    def _get_result_route_indices(self, data):
        routes = data["result"]["routes"]
        if len(routes) == 0:
            return []
        else:
            return [route["index"] for route in routes]

    def _get_result(self, data, all_routes):
        if isinstance(all_routes, Routes):
            all_routes = all_routes.to_dict()
        result_routes_indices = self._get_result_route_indices(data)
        result = Routes(
            routes=[Route(**all_routes[i], index=i) for i in result_routes_indices]
        )
        return result

    def to_dict(self):

        return {"result": self.result.to_dict()}

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=INDENT)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT)
