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
