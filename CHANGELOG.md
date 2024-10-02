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
- Upgrade CI modules
  - `actions/setup-python@v2` -> `actions/setup-python@v5`
  - `actions/checkout@v3` -> `actions/checkout@v4`
  - `actions/upload-artifact@v2` -> `actions/upload-artifact@v4`

## 1.0.0
- Initial release