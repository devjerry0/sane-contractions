from textsearch import TextSearch


class _State:
    contractions_dict: dict[str, str] | None = None
    leftovers_dict: dict[str, str] | None = None
    slang_dict: dict[str, str] | None = None

    ts_leftovers: TextSearch | None = None
    ts_leftovers_slang: TextSearch | None = None
    ts_slang: TextSearch | None = None
    ts_basic: TextSearch | None = None
    ts_view_window: TextSearch | None = None

