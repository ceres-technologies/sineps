import json

from ._exceptions import FilterExtractorError
from ._rest_adapter import Result


class FilterExtractorResponse:
    def __init__(self, result: Result):
        self.data = result.data
        self.filter = self._get_filter()

    def _get_filter(self):
        filter = self.data["result"]
        return filter
