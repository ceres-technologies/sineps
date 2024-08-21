import json
from ._exceptions import FilterExtractorError
from ._rest_adapter import Response

INDENT = 2


class Filter:
    def __init__(self, operator, value: str):
        self.type = "Filter"
        self.operator = operator
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "operator": self.operator,
            "value": self.value,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=INDENT)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT)


class ConjunctedFilter:
    def __init__(self, conjunction, filters_dict):
        self.type = "ConjunctedFilter"
        self.conjunction = conjunction
        self.filters = self._get_filters(filters_dict)

    def _get_filters(self, filters_dict):
        filters = []
        for filter in filters_dict:
            if filter["type"] == "Filter":
                filters.append(Filter(filter["operator"], filter["value"]))
            elif filter["type"] == "ConjunctedFilter":
                filters.append(
                    ConjunctedFilter(filter["conjunction"], filter["filters"])
                )
            else:
                raise FilterExtractorError("Invalid filter type")
        return filters

    def to_dict(self):
        return {
            "type": self.type,
            "conjunction": self.conjunction,
            "filters": [filter.to_dict() for filter in self.filters],
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=INDENT)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT)


class FilterExtractorResponse:
    def __init__(self, response: Response):
        self.result = self._get_result(response.data)

    def _get_result(self, data):
        result_dict = data["result"]
        if result_dict == {}:
            return {}

        if result_dict["type"] == "ConjunctedFilter":
            result = ConjunctedFilter(
                conjunction=result_dict["conjunction"],
                filters_dict=result_dict["filters"],
            )
        elif result_dict["type"] == "Filter":
            result = Filter(
                operator=result_dict["operator"],
                value=result_dict["value"],
            )
        else:
            raise FilterExtractorError("Invalid filter type")

        return result

    def to_dict(self):
        return {"result": self.result.to_dict()}

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=INDENT)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT)
