You are assisting a backup administrator who needs to audit a large set of historical backups.

In the directory `/home/user/backup_vault/`, there are several nested subdirectories containing backup archives in `.zip` and `.tar.gz` formats. However, due to a previous storage failure, some of these archives are corrupted. 

Your task is to write and execute a Python script that traverses the `/home/user/backup_vault/` directory and generates a single CSV manifest file at `/home/user/manifest.csv`.

For every `.zip` and `.tar.gz` file found in the vault (search recursively), your script must:
1. Attempt to verify the integrity of the archive (i.e., ensure it is a valid zip or gzip-compressed tar archive that can be opened and read without errors).
2. Calculate the SHA256 checksum of the archive file itself.
3. If the archive is valid, extract the `archive_id` from a file named `metadata.json` located at the root inside the archive. (Every valid archive contains this file, which is a JSON object like `{"archive_id": "..."}`).
4. If the archive is corrupted or invalid, the `archive_id` should be recorded as `UNKNOWN`.

The final output must be written to `/home/user/manifest.csv` with the following requirements:
- The first line must be exactly the header: `Filepath,Archive-ID,SHA256,Status`
- `Filepath` must be the absolute path to the archive file.
- `Status` must be either `VALID` or `CORRUPT`.
- The rows must be sorted alphabetically by `Filepath`.

Please create the script, run it, and ensure `/home/user/manifest.csv` is generated perfectly.