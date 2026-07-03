You are acting as a backup administrator rescuing data from a partially corrupted storage vault. 

A previous system dumped backup blobs into a directory tree without extensions. You have a metadata file, but you suspect some of the backup blobs are corrupted and no longer valid gzip archives.

Here is what you need to do:
1. Parse the JSON metadata file located at `/home/user/backup_catalog.json`. This file contains an array of objects, each with `file_id`, `owner`, and `timestamp` keys.
2. Identify all `file_id`s where the `owner` is exactly `"alice_admin"`.
3. Search through the directory tree at `/home/user/backup_vault/` to find the files named precisely as the identified `file_id`s. Note that files might be nested in subdirectories.
4. For each located file belonging to `alice_admin`, verify if it is a valid GZIP archive. You must do this by checking the file's binary header (magic bytes). A valid GZIP file must start with the hex bytes `1f 8b`.
5. For all valid GZIP backups belonging to `alice_admin`:
   a) Create an uncompressed tar archive at `/home/user/alice_recovery.tar` containing these valid files. (The files inside the tar should not include the full `/home/user/backup_vault/` path, just the file name or relative path from the vault root is fine, but flat structure is preferred).
   b) Generate a CSV report at `/home/user/recovery_log.csv` with the exact headers: `file_id,original_path`. List the ID and the absolute path to each valid file you found.

Write and execute a Python script to automate this extraction and verification process. Do not include files that fail the GZIP magic byte check or belong to other users.