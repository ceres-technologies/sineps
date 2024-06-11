from typing import List

from .rest_adapter import Result


class Route:
    def __init__(
        self, index: int, name: str, description: str, utterances: List[str] = []
    ):
        self.index = index
        self.name = name
        self.description = description
        self.utterances = utterances


class Routes:
    def __init__(self, routes: List[Route]):
        self.routes = routes


class IntentRouterResponse:
    def __init__(self, result: Result, all_routes: List[dict]):
        self.data = result.data
        self.all_routes = all_routes
        self.chosen = self._get_chosen()

    def _get_chosen(self):
        chosen_route_index = self.data["result"]
        chosen = Routes(
            routes=[Route(index=i, **self.all_routes[i]) for i in chosen_route_index]
        )
        return chosen
