You are acting as a backup administrator. You need to write a Python script that securely archives a directory, generates a checksum manifest, and splits the archive into transportable chunks.

Write a Python script at `/home/user/secure_backup.py` and run it to perform the following operations:

1. Target Directory: `/home/user/source_data`
2. First, traverse the target directory recursively. Compute the SHA-256 hash of every file.
3. Save these hashes into a JSON formatted manifest file at `/home/user/manifest.json`. The JSON should be a single dictionary where the keys are the file paths relative to `/home/user/source_data` (e.g., `"logs/app.log"`) and the values are the hexadecimal SHA-256 hashes.
4. Next, create a standard, uncompressed tar archive of the `/home/user/source_data` directory at `/home/user/backup.tar`. The relative paths inside the tar archive should match the structure (e.g., extracting it in an empty directory should recreate the `source_data` folder or its contents directly, but for consistency, ensure the files are archived such that their paths in the tarball match the keys in your manifest, or are prefixed with `source_data/`). Specifically, archive the directory so that the root entries in the tarball are the contents of `source_data` (e.g. `logs/app.log`, not `source_data/logs/app.log`).
5. Calculate the SHA-256 hash of the generated `/home/user/backup.tar` file and write this hex digest to a text file at `/home/user/backup_hash.txt`.
6. Finally, split `/home/user/backup.tar` into equal-sized chunks of exactly 512,000 bytes (except the last chunk, which may be smaller). Name the chunks `/home/user/backup.tar.chunk001`, `/home/user/backup.tar.chunk002`, and so on.

Once you have written the script, execute it so that all the required output files (`manifest.json`, `backup.tar`, `backup_hash.txt`, and the chunk files) are generated in `/home/user/`.