import json
import pkgutil
from itertools import product

from textsearch import TextSearch

json_open = pkgutil.get_data("contractions", "data/contractions_dict.json")
assert json_open is not None
contractions_dict = json.loads(json_open.decode("utf-8"))

json_open = pkgutil.get_data("contractions", "data/leftovers_dict.json")
assert json_open is not None
leftovers_dict = json.loads(json_open.decode("utf-8"))

json_open = pkgutil.get_data("contractions", "data/slang_dict.json")
assert json_open is not None
slang_dict = json.loads(json_open.decode("utf-8"))

for month in [
    "january",
    "february",
    "march",
    "april",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]:
    contractions_dict[month[:3] + "."] = month

contractions_dict |= {k.replace("'", "'"): v for k, v in contractions_dict.items()}

leftovers_dict |= {k.replace("'", "'"): v for k, v in leftovers_dict.items()}

safety_keys = frozenset(
    ("he's", "he'll", "we'll", "we'd", "it's", "i'd", "we'd", "we're", "i'll", "who're", "o'")
)


def get_combinations(tokens, joiners):
    option = [[x] for x in tokens]
    option = intersperse(option, joiners)
    return ["".join(c) for c in product(*option)]


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


unsafe_dict = {}
for k, v in contractions_dict.items():
    k_lower = k.lower()
    if k_lower not in safety_keys and "'" in k:
        for comb in get_combinations(k.split("'"), ["", "'"]):
            unsafe_dict[comb] = v

slang_dict.update(unsafe_dict)

ts_leftovers = TextSearch("insensitive", "norm")
ts_leftovers.add(contractions_dict)
ts_leftovers.add(leftovers_dict)

ts_leftovers_slang = TextSearch("insensitive", "norm")
ts_leftovers_slang.add(contractions_dict)
ts_leftovers_slang.add(leftovers_dict)
ts_leftovers_slang.add(slang_dict)

ts_slang = TextSearch("insensitive", "norm")
ts_slang.add(contractions_dict)
ts_slang.add(slang_dict)

ts_basic = TextSearch("insensitive", "norm")
ts_basic.add(contractions_dict)

ts_view_window = TextSearch("insensitive", "object")
ts_view_window.add([*contractions_dict.keys(), *leftovers_dict.keys(), *slang_dict.keys()])

replacers = {
    (True, False): ts_leftovers,
    (True, True): ts_leftovers_slang,
    (False, True): ts_slang,
    (False, False): ts_basic,
}


def fix(s, leftovers=True, slang=True):
    ts = replacers[(leftovers, slang)]
    return ts.replace(s)

