"""
codesign.py: Sign a file or directory with a given identity
"""

import logging
import subprocess

from pathlib import Path

BIN_CODESIGN = "/usr/bin/codesign"
BIN_SECURITY = "/usr/bin/security"


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
        arguments:    list - The arguments to use for signing
    """
    def __init__(self, file: str, identity: str, entitlements: str = None, options: list = ["runtime"], arguments: list = ["--force", "--verify", "--verbose", "--timestamp"]) -> None:
        self._file     = file
        self._identity = identity
        self._entitlements = entitlements
        self._options = options
        self._arguments = arguments


    def is_signing_identity_valid(self) -> bool:
        """
        Check if the signing identity is valid
        """
        result = subprocess.run([BIN_SECURITY, "find-identity", "-v", "-p", "codesigning"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error fetching signing identities: {result.stderr.decode('utf-8')}")
            return False

        return self._identity in result.stdout.decode("utf-8")


    def current_signing_authorities(self) -> list[str]:
        """
        Check the binary's current signing authorities

        Returns:
            list: The current signing authorities

        Sample output:
        [
            "Developer ID Application: My Organization (X1X2Y3Y4Z5Z6)",
            "Developer ID Certification Authority",
            "Apple Root CA",
        ]
        """
        result = subprocess.run([BIN_CODESIGN, "--display", "--verbose=4", self._file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error fetching current signing identity: {result.stderr.decode('utf-8')}")
            return []
        output = result.stdout.decode("utf-8")
        if "Signature=adhoc" in output:
            return "adhoc"

        identities = []
        for line in output.split("\n"):
            if "Authority=" in line:
                identities.append(line[10:])

        return identities


    def codesign_arguments(self) -> list:
        """
        Generate codesign arguments
        """
        self._file = Path(self._file).resolve()

        arguments = [BIN_CODESIGN] + self._arguments + ["--sign", self._identity, self._file]

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

        return arguments


    def sign(self) -> None:
        """
        Sign the file
        """
        if not self.is_signing_identity_valid():
            logging.error(f"Error: Signing identity {self._identity} not found")
            raise SigningIdentityNotFound(f"Signing identity not found: {self._identity}")

        logging.info(f"Signing {self._file}")
        result = subprocess.run(self.codesign_arguments(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error signing: {result.stderr.decode('utf-8')}")
            raise SigningFailed("Signing failed")
