You are acting as a backup administrator managing a daily archive pipeline. 

You have been given a directory of unnormalized user files at `/home/user/raw_data/`. Before these files can be securely archived, you need to normalize their filenames, generate a verification manifest, and package them into a compressed archive.

Please complete the following steps:

1. Write and execute a Python script that bulk-renames all files inside `/home/user/raw_data/` in-place according to these rules:
   - The entire filename (including extension) must be converted to lowercase.
   - Any spaces (` `) or underscores (`_`) must be replaced with hyphens (`-`).
   - Example: `Financial_Report 2023.XLS` becomes `financial-report-2023.xls`.

2. After renaming, generate a SHA-256 checksum manifest of the files in `/home/user/raw_data/`. 
   - The manifest must be saved at `/home/user/checksums.sha256`.
   - The format must exactly match the output of the standard `sha256sum` command (i.e., `[hash]  [filename]`, with two spaces between the hash and the filename). Only the basenames of the files should appear in the manifest, not the full paths.

3. Finally, create a gzip-compressed tarball at `/home/user/secure_backup.tar.gz`.
   - The archive must contain the `raw_data` directory (and its renamed contents) and the `checksums.sha256` file at its root. 
   - When extracting the archive, it should produce exactly `./raw_data/` and `./checksums.sha256`.

Make sure you do not leave any temporary files in `/home/user/` other than the required final files.