import os

from src.flintai import __version__
from src.flintai.locations import (
    get_major_minor_version,
)

def get_flintai_version():
    flintai_pkg_dir = os.path.join(os.path.dirname(__file__), "..", "..")
    flintai_pkg_dir = os.path.abspath(flintai_pkg_dir)

    return (
        'flintai {} from {} (python {})'.format(
            __version__, flintai_pkg_dir, get_major_minor_version(),
        )
    )