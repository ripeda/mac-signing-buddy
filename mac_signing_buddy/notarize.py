"""
notarize.py: Notarize a file through Apple's notarization service
"""

import logging
import subprocess


class NotarizationFailed(Exception):
    """
    Exception raised when the notarization process fails
    """
    pass

class NotarizationFilePreparationFailed(Exception):
    """
    Exception raised when the file preparation for notarization fails
    """
    pass


class Notarize:
    """
    Parameters:
        file:     str - The file to notarize (File or Bundle)
        apple_id: str - The Apple ID to use for notarization
        password: str - The password for the Apple ID
        team_id:  str - The Team ID to use for notarization
        output:   str - The output file name (Optional, defaults to <file>.zip)
    """
    def __init__(self, file: str, apple_id: str, password: str, team_id: str, output: str = None) -> None:
        self._file     = file
        self._apple_id = apple_id
        self._password = password
        self._team_id  = team_id
        self._output   = f"{self._file}.zip"
        if output is not None:
            self._output = output


    def _prepare_file(self) -> None:
        """
        Prepare the file for notarization
        """
        logging.info(f"Preparing {self._file} for notarization")
        result = subprocess.run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", self._file, self._output], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error preparing file: {result.stderr.decode('utf-8')}")
            raise NotarizationFilePreparationFailed(f"File preparation failed: {result.stderr.decode('utf-8')}")


    def _decode_id_from_stdout(self, stdout: str) -> str:
        """
        Extract the ID from the stdout
        """
        for line in stdout.split("\n"):
            if line.startswith("  id: "):
                return line[6:]
        return None


    def _fetch_error(self, id: str) -> str:
        """
        Retrieve the error message
        """
        result = subprocess.run(["xcrun", "notarytool", "log", id, "--apple-id", self._apple_id, "--password", self._password, "--team-id", self._team_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            return result.stderr.decode("utf-8")
        return result.stdout.decode("utf-8")


    def sign(self) -> None:
        """
        Sign the file
        """

        self._prepare_file()
        logging.info(f"Uploading {self._output} for notarization")

        arguments = [
            "xcrun", "notarytool", "submit", self._output, "--apple-id", self._apple_id, "--password", self._password, "--team-id", self._team_id, "--wait"
        ]
        result = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.error(f"Error notarizing: {result.stderr.decode('utf-8')}")
            raise NotarizationFailed(f"Notarization failed: {result.stderr.decode('utf-8')}")
        if "status: Accepted" not in result.stdout.decode("utf-8"):
            error = self._fetch_error(self._decode_id_from_stdout(result.stdout.decode("utf-8")))
            logging.error(error)
            raise NotarizationFailed(f"Notarization failed: {error}")