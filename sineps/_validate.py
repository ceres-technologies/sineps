from ._exceptions import (
    InvalidFilterExtractorFormatException,
    InvalidIntentRouterFormatException,
)
from ._config import CONFIG

CONFIG_INTENT_ROUTER = CONFIG["intent_router"]
CONFIG_FILTER_EXTRACTOR = CONFIG["filter_extractor"]


def validate_intent_router_format(query, routes, allow_none):
    validate_intent_router_query(query)
    validate_intent_router_allow_none(allow_none)
    validate_routes(routes)


def validate_filter_extractor_format(query, field, required):
    validate_filter_extractor_query(query)
    validate_filter_extractor_required(required)
    validate_field(field)


def validate_intent_router_allow_none(allow_none):
    if not isinstance(allow_none, bool):
        raise InvalidIntentRouterFormatException(
            "The 'allow_none' parameter must be a boolean"
        )


def validate_intent_router_query(query):
    if not isinstance(query, str):
        raise InvalidIntentRouterFormatException("The 'query' must be a string")
    max_query_length = CONFIG_INTENT_ROUTER["max_query_length"]
    if len(query) > max_query_length:
        raise InvalidIntentRouterFormatException("Too long query")


def validate_routes(routes):
    if not isinstance(routes, list):
        raise InvalidIntentRouterFormatException("The 'routes' must be a list")
    if len(routes) == 0:
        raise InvalidIntentRouterFormatException("At least one route must be provided")
    max_routes_num = CONFIG_INTENT_ROUTER["max_routes_num"]
    if len(routes) > max_routes_num:
        raise InvalidIntentRouterFormatException(
            f"Too many routes ({len(routes)} routes > {max_routes_num} routes)"
        )
    for route_index, route in enumerate(routes):
        validate_route(route, route_index)


def validate_route(route_dict: dict, route_index: int):
    required_keys = ["name", "description"]
    optional_keys = ["utterances"]

    for key in required_keys:
        if key not in route_dict:
            raise InvalidIntentRouterFormatException(
                f"routes[{route_index}]: Missing required key: '{key}'"
            )
        if not isinstance(route_dict[key], str):
            raise InvalidIntentRouterFormatException(
                f"routes[{route_index}]: Value for key '{key}' must be a string"
            )

    max_route_name_length = CONFIG_INTENT_ROUTER["max_route_name_length"]
    if len(route_dict["name"]) > max_route_name_length:
        raise InvalidIntentRouterFormatException(
            f"Too long routes[{route_index}]'s name"
        )
    max_route_description_length = CONFIG_INTENT_ROUTER["max_route_description_length"]
    if len(route_dict["description"]) > max_route_description_length:
        raise InvalidIntentRouterFormatException(
            f"Too long routes[{route_index}]'s description"
        )

    if "utterances" in route_dict:
        if not isinstance(route_dict["utterances"], list) or not all(
            isinstance(item, str) for item in route_dict["utterances"]
        ):
            raise InvalidIntentRouterFormatException(
                f"routes[{route_index}]: Value for key 'utterances' must be a list of strings"
            )
        max_route_utterances_num = CONFIG_INTENT_ROUTER["max_route_utterances_num"]
        if len(route_dict["utterances"]) > max_route_utterances_num:
            raise InvalidIntentRouterFormatException(
                f"Too many utterances in routes[{route_index}]"
            )

        max_route_utterance_length = CONFIG_INTENT_ROUTER["max_route_utterance_length"]
        for utterance_index, utterance in enumerate(route_dict["utterances"]):
            if len(utterance) > max_route_utterance_length:
                raise InvalidIntentRouterFormatException(
                    f"Too long utterances[{utterance_index}] of routes[{route_index}]"
                )

    for key in route_dict.keys():
        if key not in required_keys and key not in optional_keys:
            raise InvalidIntentRouterFormatException(f"Unexpected key: {key}")


def validate_filter_extractor_query(query):
    if not isinstance(query, str):
        raise InvalidFilterExtractorFormatException("The query must be a string.")
    max_query_length = CONFIG_FILTER_EXTRACTOR["max_query_length"]
    if len(query) > max_query_length:
        raise InvalidFilterExtractorFormatException("Too long query.")


def validate_filter_extractor_required(required):
    if not isinstance(required, bool):
        raise InvalidFilterExtractorFormatException(
            "The 'required' parameter must be a boolean."
        )


def validate_field(field_dict):
    if not isinstance(field_dict, dict):
        raise InvalidFilterExtractorFormatException("The 'field' must be a dictionary.")
    required_keys = {"name", "description", "type"}
    optional_key = "values"
    allowed_types = {"string", "number", "list", "date"}
    allowed_types_for_values = {"list", "string"}

    for key in required_keys:
        if key not in field_dict:
            raise InvalidFilterExtractorFormatException(f"Missing required key: {key}.")

    for key in field_dict:
        if key not in required_keys and key != optional_key:
            raise InvalidFilterExtractorFormatException(f"Unexpected key: {key}.")

    if not isinstance(field_dict["name"], str):
        raise InvalidFilterExtractorFormatException(
            "The value of 'name' must be a string."
        )

    max_field_name_legnth = CONFIG_FILTER_EXTRACTOR["max_field_name_legnth"]
    if len(field_dict["name"]) > max_field_name_legnth:
        raise InvalidFilterExtractorFormatException("Too long field name")

    if not isinstance(field_dict["description"], str):
        raise InvalidFilterExtractorFormatException(
            "The value of 'description' must be a string."
        )

    max_field_description_length = CONFIG_FILTER_EXTRACTOR[
        "max_field_description_length"
    ]
    if len(field_dict["description"]) > max_field_description_length:
        raise InvalidFilterExtractorFormatException("Too long field description")

    if optional_key in field_dict:

        if not isinstance(field_dict["type"], str):
            raise InvalidFilterExtractorFormatException(
                f"The value of 'type' must be one of {allowed_types}."
            )
        if field_dict["type"] not in allowed_types:
            raise InvalidFilterExtractorFormatException(
                f"The value of 'type' must be one of {allowed_types}."
            )

        if not field_dict["type"] in allowed_types_for_values:
            raise InvalidFilterExtractorFormatException(
                f"The 'value' parameter is not allowed when the field type is '{field_dict['type']}'."
            )
        if not isinstance(field_dict[optional_key], list):
            raise InvalidFilterExtractorFormatException(
                f"The value of '{optional_key}' must be a list of strings."
            )
        if not all(isinstance(item, str) for item in field_dict[optional_key]):
            raise InvalidFilterExtractorFormatException(
                f"All elements in the '{optional_key}' list must be strings."
            )

        if (
            len(field_dict[optional_key])
            > CONFIG_FILTER_EXTRACTOR["max_field_values_num"]
        ):
            raise InvalidFilterExtractorFormatException(
                f"Too many values ({len(field_dict[optional_key])} values > {CONFIG_FILTER_EXTRACTOR['max_field_values_num']} values)"
            )

        for value_index, value in enumerate(field_dict[optional_key]):
            max_field_value_length = CONFIG_FILTER_EXTRACTOR["max_field_value_length"]
            if len(value) > max_field_value_length:
                raise InvalidFilterExtractorFormatException(
                    f"Too long values[{value_index}] string"
                )
