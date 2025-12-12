import json
import pkgutil


def load_json_data(filename: str) -> dict[str, str] | list[str]:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    assert json_bytes is not None
    return json.loads(json_bytes.decode("utf-8"))

