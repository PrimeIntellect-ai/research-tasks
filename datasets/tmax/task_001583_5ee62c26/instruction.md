You are acting as a storage administrator. We are running out of disk space on our primary backup volume. A legacy backup system dumped a large number of archive files (`.zip` and `.tar.gz`) scattered across a deep, nested directory structure at `/home/user/legacy_backups/`. 

We suspect many of these archives are corrupted or incomplete due to network interruptions during the legacy backup process. Furthermore, the naming convention is a complete mess, making deduplication impossible.

Your task is to write and execute a script (in the language of your choice) to clean up this storage array. 

Here are your exact requirements:

1. **Recursive Traversal**: Traverse the `/home/user/legacy_backups/` directory recursively to find all `.zip` and `.tar.gz` files.
2. **Integrity Verification**: 
   - Test every archive for integrity. 
   - A `.zip` is valid if it passes a standard integrity check (e.g., `unzip -t`).
   - A `.tar.gz` is valid if its gzip compression and tar structure are intact (e.g., `tar -tzf`).
3. **Corrupt Files**: If an archive fails the integrity check, **delete** it from the filesystem immediately to free up space.
4. **Valid Files & Bulk Renaming**:
   - If an archive is valid, calculate the SHA-256 hash of the file.
   - Rename the file to the format `backup_<sha256>.<ext>`, where `<sha256>` is the full 64-character lowercase hex digest, and `<ext>` is the original extension (`zip` or `tar.gz`).
   - Move the renamed file to a new flattened directory: `/home/user/clean_backups/`. (Create this directory if it doesn't exist).
5. **Reporting**: Create a JSON report at `/home/user/backup_report.json` containing the exact results of your operation. It must strictly follow this format:

```json
{
  "processed": <total_archives_found>,
  "valid_moved": <number_of_valid_archives>,
  "corrupt_deleted": <number_of_corrupt_archives>,
  "valid_files": [
    "<new_name_1.zip>",
    "<new_name_2.tar.gz>"
  ],
  "corrupt_files": [
    "<original_corrupt_name_1.zip>"
  ]
}
```
*Note: The arrays `valid_files` and `corrupt_files` should be sorted alphabetically by filename.*

Do not leave any valid archives in `/home/user/legacy_backups/`. Ensure your script handles edge cases gracefully and cleans up the storage space effectively.