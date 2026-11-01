# Prepare USB transfer package

- **Prompt execution date and time:** 2026-10-31 15:07:10 +01:00 (Europe/Sarajevo)
- **Original prompt:**

  > To bi bilo najbolje. Kako si rekao. Možemo to odraditi preko stika ili ako možeš u GUI okruženju pošto smo uvezali računare?

## Task

Choose a safe transfer method for the desktop database data and uploaded media, and prepare the desktop-side package for transfer to the laptop.

## Changes made

- Reviewed the official Codex/ChatGPT project and remote-connection documentation to distinguish conversation synchronization and remote control from bulk local file transfer.
- Chose a hybrid workflow: use a USB drive for the approximately 508 MiB payload and use the Codex GUI to coordinate and execute the laptop-side restore.
- Attempted a PostgreSQL custom-format dump, then stopped using that approach after `pg_dump` encountered a permission error on the extension-owned `pointcloud_formats` table. The desktop database has many extensions that are not needed for the application data and would complicate a PostgreSQL 18-to-16 restore.
- Created a valid UTF-8 Django fixture at `backups/laptop-transfer-20261031/wiki_groblje_appdata_utf8.json` without changing the database. It contains 478 objects and was parsed successfully.
- Confirmed fixture content counts against both Django ORM and direct SQL results: 14 cemeteries, 62 graves, 66 persons, 85 grave photos, and 12 cemetery photos.
- Created `backups/laptop-transfer-20261031/wiki_groblje_media.zip` from the complete desktop `media/` tree.
- Validated the ZIP against the source: 211 files, 534,490,601 source bytes, and no path differences.
- Calculated SHA-256 hashes for the two valid transfer files and recorded them in `backups/laptop-transfer-20261031/TRANSFER_README.md`.
- Clearly marked `wiki_groblje_pg18.dump` and `wiki_groblje_appdata.json` as incomplete and prohibited for transfer or restore. The restricted session did not permit deleting the incomplete files.
- Did not write to the USB drive, mutate the desktop database, alter the source media files, or change the laptop.

## Reasons for implementation decisions

- The GUI connection is suitable for coordinating work on the laptop, but it does not make the desktop project folder available as a bulk file-transfer channel.
- A physical USB transfer is simple, fast, and has sufficient capacity for this payload.
- A Django fixture transfers the application data without importing unnecessary desktop PostgreSQL extensions or relying on a PostgreSQL 18 dump restoring into PostgreSQL 16.
- Preserving the laptop's current database by renaming it before restoration provides a recoverable rollback path.
- Hashes and archive path comparison provide independent checks that the payload remains intact during the USB transfer.

## Related reports

- [00055_plan_desktop_data_and_media_copy.md](00055_plan_desktop_data_and_media_copy.md)
- [00054_confirm_laptop_database_locale_cause.md](00054_confirm_laptop_database_locale_cause.md)
- Follow-up laptop restore report: not yet created.
