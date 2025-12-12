from .data_io import load_json_data
from .transforms import build_apostrophe_variants, normalize_apostrophes


def load_all_contractions() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    contractions_dict: dict[str, str] = load_json_data("contractions_dict.json")  # type: ignore[assignment]
    leftovers_dict: dict[str, str] = load_json_data("leftovers_dict.json")  # type: ignore[assignment]
    slang_dict: dict[str, str] = load_json_data("slang_dict.json")  # type: ignore[assignment]
    safety_keys_list: list[str] = load_json_data("safety_keys.json")  # type: ignore[assignment]
    safety_keys = frozenset(safety_keys_list)

    contractions_dict |= normalize_apostrophes(contractions_dict)
    leftovers_dict |= normalize_apostrophes(leftovers_dict)

    unsafe_dict = build_apostrophe_variants(contractions_dict, safety_keys)
    slang_dict.update(unsafe_dict)

    return contractions_dict, leftovers_dict, slang_dict
