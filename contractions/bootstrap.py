from __future__ import annotations

from .file_loader import load_dict_data, load_list_data
from .transformer import build_apostrophe_variants, normalize_apostrophes


def load_all_contractions() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    contractions_dict = load_dict_data("contractions_dict.json")
    leftovers_dict = load_dict_data("leftovers_dict.json")
    slang_dict = load_dict_data("slang_dict.json")
    safety_keys = frozenset(load_list_data("safety_keys.json"))

    contractions_dict |= normalize_apostrophes(contractions_dict)
    leftovers_dict |= normalize_apostrophes(leftovers_dict)

    unsafe_dict = build_apostrophe_variants(contractions_dict, safety_keys)
    slang_dict.update(unsafe_dict)

    return contractions_dict, leftovers_dict, slang_dict
