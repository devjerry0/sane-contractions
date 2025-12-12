import pytest

from contractions.data_io import load_dict_data, load_list_data


def test_load_dict_data():
    result = load_dict_data("contractions_dict.json")
    assert isinstance(result, dict)
    assert len(result) > 0


def test_load_list_data():
    result = load_list_data("safety_keys.json")
    assert isinstance(result, list)
    assert len(result) > 0


def test_load_dict_data_returns_none():
    import contractions.data_io as data_io_module
    import pkgutil
    original = pkgutil.get_data

    def mock_get_data(package, resource):
        return None

    pkgutil.get_data = mock_get_data
    try:
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            load_dict_data("test.json")
    finally:
        pkgutil.get_data = original


def test_load_dict_data_wrong_type():
    with pytest.raises(TypeError, match="Expected dict"):
        load_dict_data("safety_keys.json")


def test_load_list_data_returns_none():
    import contractions.data_io as data_io_module
    import pkgutil
    original = pkgutil.get_data

    def mock_get_data(package, resource):
        return None

    pkgutil.get_data = mock_get_data
    try:
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            load_list_data("test.json")
    finally:
        pkgutil.get_data = original


def test_load_list_data_wrong_type():
    with pytest.raises(TypeError, match="Expected list"):
        load_list_data("contractions_dict.json")

