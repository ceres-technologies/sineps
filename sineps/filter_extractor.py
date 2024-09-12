import json
from ._exceptions import FilterExtractorError
from ._rest_adapter import Response
import re
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


INDENT = 2


def calculate_date(current_date: date, expression: str) -> date:
    match = re.match(r"\$\{\s*current_date\s*([+-])\s*(.*?)\s*\}", expression)
    if not match:
        raise ValueError("Wrong date expression format.")
    operation = match.group(1)
    changes = match.group(2)

    changes_matches = re.findall(r"(\d+)([ymd])", changes)

    result_date = current_date

    for change in changes_matches:
        value = int(change[0])
        unit = change[1]

        if unit == "y":
            delta = relativedelta(years=value)
        elif unit == "m":
            delta = relativedelta(months=value)
        elif unit == "d":
            delta = timedelta(days=value)
        else:
            raise ValueError("Wrong date expression format.")

        if operation == "-":
            result_date -= delta
        else:
            result_date += delta

    return result_date


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
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)


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
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)


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
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=INDENT, ensure_ascii=False)
