from importlib import resources


def test_ships_py_typed_marker() -> None:
    assert (resources.files("contractions") / "py.typed").is_file()
