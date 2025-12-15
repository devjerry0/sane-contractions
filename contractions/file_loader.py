import json
import pkgutil

from typing import cast

from .validation import validate_data_type


def load_dict_data(filename: str) -> dict[str, str]:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    if json_bytes is None:
        raise FileNotFoundError(f"Data file not found: {filename}")

    data = json.loads(json_bytes.decode("utf-8"))
    validate_data_type(data, dict, filename)

    return cast(dict[str, str], data)


def load_list_data(filename: str) -> list[str]:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    if json_bytes is None:
        raise FileNotFoundError(f"Data file not found: {filename}")

    data = json.loads(json_bytes.decode("utf-8"))
    validate_data_type(data, list, filename)

    return cast(list[str], data)

