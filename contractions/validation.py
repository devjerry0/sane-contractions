from __future__ import annotations


def validate_string_param(value: object, param_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{param_name} must be a string, got {type(value).__name__}")


def validate_non_empty_string(value: object, param_name: str) -> None:
    validate_string_param(value, param_name)
    if not value:
        raise ValueError(f"{param_name} cannot be empty")


def validate_dict_param(value: object, param_name: str) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{param_name} must be a dict, got {type(value).__name__}")


def validate_int_param(value: object, param_name: str) -> None:
    if not isinstance(value, int):
        raise TypeError(f"{param_name} must be an integer, got {type(value).__name__}")


def validate_data_type(data: object, expected_type: type, source: str) -> None:
    if not isinstance(data, expected_type):
        raise TypeError(f"Expected {expected_type.__name__} in {source}, got {type(data).__name__}")


def validate_file_contains_dict(data: object, filepath: str) -> None:
    if not isinstance(data, dict):
        raise ValueError(f"File must contain a JSON dictionary, got {type(data).__name__}")

