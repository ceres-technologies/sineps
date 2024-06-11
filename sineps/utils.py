from .exceptions import TheSinepsApiException


def add_index_to_dictionary_list(dict_list: list):
    for i, item in enumerate(dict_list):
        item["index"] = i
    return dict_list


def uppercase_keys(input_dict):
    new_dict = {}
    for key, value in input_dict.items():
        if isinstance(key, str) and key.isascii():
            new_key = key.upper()
        else:
            new_key = key
        new_dict[new_key] = value
    return new_dict


def validate_route_dict(route_dict: dict):
    required_keys = ["name", "description"]
    optional_keys = ["utterances"]

    for key in required_keys:
        if key not in route_dict:
            raise TheSinepsApiException(f"Missing required key: {key}")
        if not isinstance(route_dict[key], str):
            raise TheSinepsApiException(f"Value for key '{key}' must be a string")

    if "utterances" in route_dict:
        if not isinstance(route_dict["utterances"], list) or not all(
            isinstance(item, str) for item in route_dict["utterances"]
        ):
            raise TheSinepsApiException(
                f"Value for key 'utterances' must be a list of strings"
            )

    for key in route_dict.keys():
        if key not in required_keys and key not in optional_keys:
            raise TheSinepsApiException(f"Unexpected key: {key}")


def validate_filed_dict(filed_dict: dict):
    required_keys = {"name", "description", "type"}
    optional_key = "values"
    allowed_types = {"string", "number", "list", "date"}

    for key in required_keys:
        if key not in filed_dict:
            raise TheSinepsApiException(f"Missing required key: {key}")

    for key in filed_dict:
        if key not in required_keys and key != optional_key:
            raise TheSinepsApiException(f"Unexpected key: {key}")

    if not isinstance(filed_dict["name"], str):
        raise TheSinepsApiException("The value of 'name' must be a string")

    if not isinstance(filed_dict["description"], str):
        raise TheSinepsApiException("The value of 'description' must be a string")

    if filed_dict["type"] not in allowed_types:
        raise TheSinepsApiException(
            f"The value of 'type' must be one of {allowed_types}"
        )

    if optional_key in filed_dict:
        if not isinstance(filed_dict[optional_key], list):
            raise TheSinepsApiException(
                f"The value of '{optional_key}' must be a list of strings"
            )
        if not all(isinstance(item, str) for item in filed_dict[optional_key]):
            raise TheSinepsApiException(
                f"All elements in the '{optional_key}' list must be strings"
            )
