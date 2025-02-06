import pytest

from lib.api_util.data_helper import search_dict


def demo_id(name):
    mapped_name = search_dict(name, pytest.test_data)
    return mapped_name if mapped_name else name
