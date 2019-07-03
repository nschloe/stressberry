from .__about__ import (
    __author__,
    __email__,
    __copyright__,
    __license__,
    __version__,
    __status__,
)

from .main import stress_cpu
from . import cli

__all__ = [
    "__author__",
    "__email__",
    "__copyright__",
    "__license__",
    "__version__",
    "__status__",
    "cli",
    "stress_cpu",
]
