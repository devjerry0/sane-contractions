import warnings

from ._version import __version__
from .api import add, add_dict, e, expand, load_file, p, preview


def fix(*args, **kwargs):
    warnings.warn(
        "fix() is deprecated and will be removed in v1.0.0. Use expand() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return expand(*args, **kwargs)


__all__ = ["expand", "fix", "add", "add_dict", "load_file", "preview", "e", "p", "__version__"]
