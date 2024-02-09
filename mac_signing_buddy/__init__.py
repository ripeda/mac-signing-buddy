"""
mac_signing_buddy is a Python package that provides a simple interface to
Apple's codesign and notarization tools.
"""

__title__:        str = "mac_signing_buddy"
__version__:      str = "1.0.0"
__description__:  str = "A Python package to sign and notarize macOS applications."
__url__:          str = "https://github.com/ripeda/mac-signing-buddy"
__license__:      str = "3-clause BSD License"
__author__:       str = "RIPEDA Consulting"
__author_email__: str = "info@ripeda.com"
__status__:       str = "Production/Stable"
__all__:         list = ["Sign", "Notarize"]

from .codesign import Sign, SigningIdentityNotFound, SigningFailed
from .notarize import Notarize
from .cli import main