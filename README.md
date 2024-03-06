# Mac Signing Buddy

Python module to easily sign Mac applications.


## Usage - CLI

```bash
python3 -m mac_signing_buddy \
    --identity "$signing_identity" \
    --apple-id "$notarize_apple_id" \
    --password "$notarize_password" \
    --team-id "$notarize_team_id" \
    --entitlements "$entitlements" \
    --file "$file_to_sign"
```

## Usage - Python

```python
from mac_signing_buddy import Sign, Notarize

file = "path/to/file"
entitlements = "path/to/entitlements.plist"

identity = "Developer ID Application: Your Name (XXXXXXXXXX)"
apple_id = "sjobs@apple.com"
password = "password"
team_id  = "XXXXXXXXXX"

sign_obj = Sign(file, identity, entitlements)
sign_obj.sign()

notarize_obj = Notarize(file, apple_id, password, team_id, output)
notarize_obj.sign()
```