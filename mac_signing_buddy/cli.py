"""
cli.py: Command line interface for the macOS Signing Buddy
"""
import sys
import logging
import argparse

from . import Sign
from . import Notarize


def _set_generic_logger():
    """
    Set a generic logger
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")


def main():
    """
    Main entry point
    """
    _set_generic_logger()

    parser = argparse.ArgumentParser(description="macOS Signing Buddy")

    parser.add_argument("--file",         help="The file or directory to sign or notarize", required=True)
    parser.add_argument("--identity",     help="The identity to use for signing", required=False)
    parser.add_argument("--entitlements", help="The entitlements file to use for signing", required=False)
    parser.add_argument("--apple-id",     help="The Apple ID to use for notarization", required=False)
    parser.add_argument("--password",     help="The password for the Apple ID", required=False)
    parser.add_argument("--team-id",      help="The Team ID to use for notarization", required=False)
    parser.add_argument("--output",       help="The output file name (Optional, defaults to <file>.zip)", required=False)

    args = parser.parse_args()

    if args.identity is not None:
        sign_obj = Sign(args.file, args.identity, args.entitlements)
        sign_obj.sign()

    if all([args.apple_id, args.password, args.team_id, args.file]):
        notarize_obj = Notarize(args.file, args.apple_id, args.password, args.team_id, args.output)
        notarize_obj.sign()
