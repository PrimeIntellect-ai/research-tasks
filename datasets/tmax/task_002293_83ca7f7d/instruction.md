You are a backup administrator tasked with migrating legacy backup archives to a new format. 

The legacy backups are located in `/home/user/legacy_archive/`. Inside this directory, there are multiple subdirectories, each representing a distinct backup (e.g., `backup_alpha`, `backup_beta`).
Inside each backup directory, the backup payload has been split into multiple chunks named `chunk_aa`, `chunk_ab`, `chunk_ac`, etc.

**Legacy Backup Format:**
When a backup's chunks are merged in alphabetical order, the resulting binary file has the following structure:
1. **Header:** The first exactly 8 bytes are a custom binary timestamp/identifier.
2. **Payload:** The remaining bytes (from byte 9 to the end) are a valid `gzip` compressed stream containing a single text file (the actual backup data).

**Your Task:**
Write and execute a Bash script at `/home/user/migrate_backup.sh` that iterates through all backup directories in `/home/user/legacy_archive/` and performs the following migration for each:

1. **Merge and Extract:** Reassemble the legacy chunks. Extract the 8-byte binary header.
2. **Decompress:** Extract and decompress the `gzip` payload into plain text.
3. **Transform:** Append a new line to the end of the decompressed text data with the exact format: `VERIFIED: <hex_header>` where `<hex_header>` is the lowercase hexadecimal representation of the 8-byte binary header (e.g., `VERIFIED: 1122334455667788`).
4. **Re-compress and Split:** Compress the transformed text data using `bzip2`. Split the resulting `bzip2` stream into exact 50KB (50 * 1024 bytes) chunks. The split chunks must be named `part_aa`, `part_ab`, etc.
5. **Atomic Staging and Commit:** 
    - Write the new chunks to a temporary staging directory (e.g., `/tmp/staging_backup_alpha/`).
    - Once all chunks for a backup are written to the staging directory, move the staging directory atomically to its final location at `/home/user/new_archive/<backup_name>/chunks/`.
    - Save the extracted 8-byte binary header to `/home/user/new_archive/<backup_name>/header.bin`.

**Requirements & Constraints:**
- The final directory structure must look exactly like this:
  `/home/user/new_archive/backup_alpha/header.bin`
  `/home/user/new_archive/backup_alpha/chunks/part_aa`
  `/home/user/new_archive/backup_alpha/chunks/part_ab` (etc.)
- The atomic move step is critical: do not write chunks directly to `/home/user/new_archive/`. You must assemble the `chunks` directory in a temporary location and `mv` it to the final destination to prevent partial archive states.
- Ensure your script completes the processing for all backups present in `/home/user/legacy_archive/`.