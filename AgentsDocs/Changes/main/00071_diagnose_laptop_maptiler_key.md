# Diagnose laptop MapTiler key

- **Prompt execution date and time:** 2026-10-31 16:26:43 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > izgleda da je sadržaj ok ali mape ne rade. Javlja invalid key

## Task

Diagnose the restored laptop application's MapTiler `invalid key` response without exposing API-key values.

## Changes made

- Confirmed from project code and documentation that public and admin map views receive `settings.MAPTILER_API_KEY`, while the base settings normally read `MAPTILER_API_KEY` from the environment.
- Confirmed that the laptop launch block supplies its process-scoped MapTiler value from `work\local-secrets.json` through `LOCAL_MAPTILER_API_KEY`, which the laptop-specific settings module consumes.
- Calculated a non-reversible fingerprint of the working desktop `.env` MapTiler value without printing the value: length 20 and SHA-256 `5941D37C524431B90A1BC64624A6DD55304E4719DA937FAEA57761658EF4C520`.
- Prepared a laptop-side read-only fingerprint check for `local-secrets.json` so the two values can be compared without disclosing either key.
- Reviewed the project's MapTiler operational notes, including key rendering, browser network requests, CORS behavior, and origin restrictions as distinct diagnostic possibilities.
- Attempted to retrieve current official MapTiler key/origin documentation, but the documentation search returned no accessible page content in this session; no unsupported current-policy claim was used as the diagnosis.
- Did not change either API key, laptop secrets, application code, database, media, server, MapTiler account, or browser configuration.

## Reasons for implementation decisions

- An `invalid key` response can result from a different, empty, revoked, or origin-restricted key, so the stored laptop value must be compared before changing code.
- Length and SHA-256 permit an exact equality check without placing the client key in chat, terminal output, reports, or Git.
- The restored database and media are independent of the map tile authentication failure and require no rollback.

## Related reports

- [00070_prepare_laptop_application_smoke_start.md](00070_prepare_laptop_application_smoke_start.md)
- [00069_confirm_laptop_restore_complete.md](00069_confirm_laptop_restore_complete.md)
- [MapTiler and coordinate handling](../../Topics/MAPTILER_AND_COORDINATES.md)
- Follow-up key repair or origin diagnosis report: not yet created.
