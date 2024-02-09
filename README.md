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