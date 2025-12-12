import json
import pkgutil
from itertools import product


def load_json_data(filename: str) -> dict | list:
    json_bytes = pkgutil.get_data("contractions", f"data/{filename}")
    assert json_bytes is not None
    return json.loads(json_bytes.decode("utf-8"))


def normalize_apostrophes(contractions: dict[str, str]) -> dict[str, str]:
    return {
        contraction.replace("'", "'"): expansion
        for contraction, expansion in contractions.items()
    }


def build_apostrophe_variants(contractions: dict[str, str], safety_keys: frozenset[str]) -> dict[str, str]:
    apostrophe_variants = ["", "'"]
    variants_dict = {}

    for contraction, expansion in contractions.items():
        if "'" not in contraction:
            continue

        if contraction.lower() in safety_keys:
            continue

        tokens = contraction.split("'")
        combinations = get_combinations(tokens, apostrophe_variants)

        for combination in combinations:
            variants_dict[combination] = expansion

    return variants_dict


def get_combinations(tokens, joiners):
    token_options = [[token] for token in tokens]
    interspersed_options = intersperse(token_options, joiners)
    return ["".join(combination) for combination in product(*interspersed_options)]


def intersperse(items, separator):
    result = [separator] * (len(items) * 2 - 1)
    result[0::2] = items
    return result


def load_all_contractions():
    contractions_dict = load_json_data("contractions_dict.json")
    leftovers_dict = load_json_data("leftovers_dict.json")
    slang_dict = load_json_data("slang_dict.json")
    safety_keys = frozenset(load_json_data("safety_keys.json"))

    contractions_dict |= normalize_apostrophes(contractions_dict)
    leftovers_dict |= normalize_apostrophes(leftovers_dict)

    unsafe_dict = build_apostrophe_variants(contractions_dict, safety_keys)
    slang_dict.update(unsafe_dict)

    return contractions_dict, leftovers_dict, slang_dict

