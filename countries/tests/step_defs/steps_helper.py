def is_str_dict_or_list(strng):
    return (strng.startswith("{") and strng.endswith("}")) or (strng.startswith("[") and strng.endswith("]"))
