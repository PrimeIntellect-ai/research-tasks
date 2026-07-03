You are acting as a storage administrator tasked with cleaning up disk space and verifying the integrity of recent backups. You have a backup log file and a directory containing binary backup blobs. Unfortunately, some backup files are corrupted (missing the correct binary header) or correspond to failed backup jobs.

Write and execute a Rust program to parse the logs, verify the binary headers, generate checksums, and safely write a manifest of valid files. 

Here are the specific details:

1. **Input Log:** There is a log file at `/home/user/backup.log`. It contains multi-line records in this exact format:
```
[RECORD START]
File: <filename>
Date: <YYYY-MM-DD>
Status: <SUCCESS|FAILED>
[RECORD END]
```
You need to extract the filenames for all records where the `Status` is exactly `SUCCESS`.

2. **Binary Header Extraction:** The backup blob files are located in `/home/user/backups/`. For each `SUCCESS` filename extracted from the log, check if the file exists in this directory. If it does, read the first 4 bytes of the file. A valid backup file must start with the exact ASCII string `BKP1` (hex `42 4B 50 31`).

3. **Checksum and Manifest Generation:** If the file exists and has the valid `BKP1` header, calculate the SHA-256 checksum of the *entire* file (including the header). 

4. **Atomic Write:** You must write the successful validations to a manifest file at `/home/user/valid_backups.manifest`. Each line should be formatted as `<filename> <sha256>`. 
To prevent partial writes from corrupting the manifest if the script crashes, you *must* perform an atomic write. Write the output to a temporary file (`/home/user/valid_backups.manifest.tmp`) first, and upon successful completion, rename it to `/home/user/valid_backups.manifest`.

Your goal is to write the Rust code (e.g., `verify.rs`), compile it, and run it to produce the final `/home/user/valid_backups.manifest` file. Ensure the Rust code handles missing files gracefully (simply skip them).