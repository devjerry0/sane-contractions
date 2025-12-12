import json
import pkgutil


def load_dict_data(filename: str) -> dict[str, str]:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    assert json_bytes is not None
    data = json.loads(json_bytes.decode("utf-8"))
    assert isinstance(data, dict)
    return data


def load_list_data(filename: str) -> list[str]:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    assert json_bytes is not None
    data = json.loads(json_bytes.decode("utf-8"))
    assert isinstance(data, list)
    return data

