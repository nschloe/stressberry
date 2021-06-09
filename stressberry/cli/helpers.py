import sys

from ..__about__ import __version__


def _get_version_text():
    return "\n".join(
        [
            "stressberry {} [Python {}.{}.{}]".format(
                __version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            "Copyright (c) 2017-2020 Nico Schlömer <nico.schloemer@gmail.com>",
        ]
    )
