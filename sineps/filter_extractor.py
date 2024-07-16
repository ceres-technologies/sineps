import json

from ._exceptions import FilterExtractorException
from ._rest_adapter import Result


class FilterExtractorResponse:
    def __init__(self, result: Result):
        self.data = result.data
        self.filter = self._get_filter()

    def _get_filter(self):
        filter_str = self.data["result"]
        try:
            filter = json.loads(filter_str)
        except json.JSONDecodeError as e:
            raise FilterExtractorException(
                "The filter in the response is not valid JSON"
            ) from e
        return filter
