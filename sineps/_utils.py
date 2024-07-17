def handle_error_message(is_success: bool, data_out: dict):
    if "detail" in data_out and not is_success:
        return data_out["detail"]
    elif is_success:
        return "Success"
    return None


def add_index_to_dictionary_list(dict_list: list):
    new_dict_list = []
    for i, item in enumerate(dict_list):
        new_item = item.copy()
        new_item["index"] = i
        new_dict_list.append(new_item)
    return new_dict_list
