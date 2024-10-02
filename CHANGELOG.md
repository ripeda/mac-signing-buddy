# Mac Signing Buddy Changelog

## 1.1.0
- Add time stamping to the signing process
- Use full path for subprocess calls
  - Avoids issues with `PATH` not being set correctly
- Add `arguments` parameter to `codesign.py` command
  - Defaults to `["--force", "--verify", "--verbose", "--timestamp"]`
- Add `codesign_arguments()` function to `codesign.py`
  - If required, easily export arguments for use in other scripts
- Avoid zipping files if input is already a zip file for notarization
- Add `.notarize()` alias to `notarize.py` for easier use

## 1.0.0
- Initial release