import pytest

from contractions.file_loader import load_dict_data, load_list_data


def test_load_dict_data() -> None:
    result = load_dict_data("contractions_dict.json")
    assert isinstance(result, dict)
    assert len(result) > 0


def test_load_list_data() -> None:
    result = load_list_data("safety_keys.json")
    assert isinstance(result, list)
    assert len(result) > 0


def test_load_dict_data_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("contractions.file_loader.pkgutil.get_data", lambda package, filename: None)
    with pytest.raises(FileNotFoundError, match=r"Data file not found: test\.json"):
        load_dict_data("test.json")


def test_load_dict_data_wrong_type() -> None:
    with pytest.raises(TypeError, match="Expected dict"):
        load_dict_data("safety_keys.json")


def test_load_list_data_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("contractions.file_loader.pkgutil.get_data", lambda package, filename: None)
    with pytest.raises(FileNotFoundError, match=r"Data file not found: test\.json"):
        load_list_data("test.json")


def test_load_list_data_wrong_type() -> None:
    with pytest.raises(TypeError, match="Expected list"):
        load_list_data("contractions_dict.json")

