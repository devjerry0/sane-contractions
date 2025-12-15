import pytest

from contractions.validation import (
    validate_data_type,
    validate_dict_param,
    validate_int_param,
    validate_non_empty_string,
    validate_string_param,
)


def test_validate_string_param_valid() -> None:
    validate_string_param("test", "param")


def test_validate_string_param_invalid() -> None:
    with pytest.raises(TypeError, match="param must be a string"):
        validate_string_param(123, "param")


def test_validate_non_empty_string_valid() -> None:
    validate_non_empty_string("test", "param")


def test_validate_non_empty_string_empty() -> None:
    with pytest.raises(ValueError, match="param cannot be empty"):
        validate_non_empty_string("", "param")


def test_validate_dict_param_valid() -> None:
    validate_dict_param({"key": "value"}, "param")


def test_validate_dict_param_invalid() -> None:
    with pytest.raises(TypeError, match="param must be a dict"):
        validate_dict_param([1, 2, 3], "param")


def test_validate_int_param_valid() -> None:
    validate_int_param(42, "param")


def test_validate_int_param_invalid() -> None:
    with pytest.raises(TypeError, match="param must be an integer"):
        validate_int_param("42", "param")


def test_validate_data_type_valid_dict() -> None:
    validate_data_type({"key": "value"}, dict, "source.json")


def test_validate_data_type_valid_list() -> None:
    validate_data_type([1, 2, 3], list, "source.json")


def test_validate_data_type_invalid() -> None:
    with pytest.raises(TypeError, match=r"Expected dict in source\.json, got list"):
        validate_data_type([1, 2, 3], dict, "source.json")

