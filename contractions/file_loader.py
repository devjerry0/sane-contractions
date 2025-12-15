from __future__ import annotations

import json
import pkgutil

from pathlib import Path
from typing import cast

from .validation import validate_data_type, validate_file_contains_dict


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


def load_dict_from_file(filepath: str) -> dict[str, str]:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found at: {filepath}")

    contractions_data = json.loads(path.read_text(encoding="utf-8"))
    validate_file_contains_dict(contractions_data, filepath)
    return cast(dict[str, str], contractions_data)


def load_dict_from_folder(folderpath: str) -> dict[str, str]:
    folder = Path(folderpath)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found at: {folderpath}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folderpath}")
    
    json_files = sorted(folder.glob("*.json"))
    
    if not json_files:
        raise ValueError(f"No JSON files found in folder: {folderpath}")
    
    merged_contractions: dict[str, str] = {}
    for json_file in json_files:
        contractions_data = json.loads(json_file.read_text(encoding="utf-8"))
        validate_file_contains_dict(contractions_data, str(json_file))
        merged_contractions.update(contractions_data)
    
    return merged_contractions

