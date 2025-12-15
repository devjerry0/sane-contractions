from __future__ import annotations

from itertools import product


def normalize_apostrophes(contractions: dict[str, str]) -> dict[str, str]:
    return {
        contraction.replace("'", "'"): expansion
        for contraction, expansion in contractions.items()
        if "'" in contraction
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
        combinations = _get_combinations(tokens, apostrophe_variants)

        for combination in combinations:
            variants_dict[combination] = expansion

    return variants_dict


def _get_combinations(tokens: list[str], joiners: list[str]) -> list[str]:
    token_options = [[token] for token in tokens]
    interspersed_options = _intersperse(token_options, joiners)
    return ["".join(combination) for combination in product(*interspersed_options)]


def _intersperse(items: list, separator: list[str]) -> list:
    num_items = len(items)
    num_separators = num_items - 1
    total_slots = num_items + num_separators

    result = [separator] * total_slots
    result[0::2] = items
    return result

