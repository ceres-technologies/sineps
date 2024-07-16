TOKEN_STRING_LENGTH_RATIO = 6.5
CONFIG = {
    "intent_router": {
        "max_query_length": 50 * TOKEN_STRING_LENGTH_RATIO,
        "max_routes_num": 5,
        "max_route_name_length": 10 * TOKEN_STRING_LENGTH_RATIO,
        "max_route_description_length": 100 * TOKEN_STRING_LENGTH_RATIO,
        "max_route_utterances_num": 50,
        "max_route_utterance_length": 50 * TOKEN_STRING_LENGTH_RATIO,
    },
    "filter_extractor": {
        "max_query_length": 50 * TOKEN_STRING_LENGTH_RATIO,
        "max_field_name_legnth": 10 * TOKEN_STRING_LENGTH_RATIO,
        "max_field_description_length": 50 * TOKEN_STRING_LENGTH_RATIO,
        "max_field_values_num": 10,
        "max_field_value_length": 50 * TOKEN_STRING_LENGTH_RATIO,
    },
}
