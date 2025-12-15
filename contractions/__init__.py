from __future__ import annotations

import warnings

from ._version import __version__
from .api import add, add_dict, e, expand, load_file, load_folder, p, preview


def fix(*args: object, **kwargs: object) -> str:
    warnings.warn(
        "fix() is deprecated and will be removed in v1.0.0. Use expand() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return expand(*args, **kwargs)  # type: ignore[arg-type]


__all__ = ["__version__", "add", "add_dict", "e", "expand", "fix", "load_file", "load_folder", "p", "preview"]
