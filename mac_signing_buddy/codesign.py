"""
codesign.py: Sign a file or directory with a given identity
"""

import logging
import subprocess

from pathlib import Path


class SigningIdentityNotFound(Exception):
    """
    Exception raised when the signing identity is not found
    """
    pass


class SigningFailed(Exception):
    """
    Exception raised when the signing process fails
    """
    pass


class Sign:
    """
    Parameters:
        file:         str  - The file or directory to sign
        identity:     str  - The identity to use for signing
        entitlements: str  - The entitlements file to use for signing
        options:      list - The options to use for signing
    """
    def __init__(self, file: str, identity: str, entitlements: str = None, options: list = ["runtime"]) -> None:
        self._file     = file
        self._identity = identity
        self._entitlements = entitlements
        self._options = options


    def is_signing_identity_valid(self) -> bool:
        """
        Check if the signing identity is valid
        """
        result = subprocess.run(["security", "find-identity", "-v", "-p", "codesigning"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error fetching signing identities: {result.stderr.decode('utf-8')}")
            return False

        return self._identity in result.stdout.decode("utf-8")


    def sign(self) -> None:
        """
        Sign the file
        """
        if not self.is_signing_identity_valid():
            logging.error(f"Error: Signing identity {self._identity} not found")
            raise SigningIdentityNotFound(f"Signing identity not found: {self._identity}")

        self._file = Path(self._file).resolve()

        logging.info(f"Signing {self._file}")
        arguments = ["codesign", "--force", "--verify", "--verbose", "--sign", self._identity, self._file]

        # Insert the --deep flag if the file is a directory
        if Path(self._file).is_dir():
            arguments.insert(1, "--deep")

        # Insert the entitlements flag if provided
        if self._entitlements is not None:
            self._entitlements = Path(self._entitlements).resolve()
            arguments.insert(1, "--entitlements")
            arguments.insert(2, self._entitlements)

        if self._options is not None:
            arguments.insert(1, f"--options={','.join(self._options)}")

        result = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error signing: {result.stderr.decode('utf-8')}")
            raise SigningFailed("Signing failed")
