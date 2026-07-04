You are a storage administrator managing disk space on a critical data volume located at `/home/user/data_volume`. The volume contains thousands of structured logs, but disk space is running low. You need to identify old, archivable files, modify their status, package them for cold storage, and clean up the active volume.

Write and execute a Bash script to perform the following operations:

1. **Metadata-based Search & Concurrency Check**: 
   Find all `.json` files in `/home/user/data_volume` (and its subdirectories) that were last modified more than 30 days ago. 
   *Rule*: The system uses a lock-file mechanism for concurrent access. If a `.json` file has a corresponding `.lock` file in the exact same directory (e.g., `record_42.json` and `record_42.json.lock`), it is currently being written to by another process and **must be skipped**, regardless of its modification date.

2. **Structured Format Parsing & Filtering**:
   For the old, unlocked files identified in step 1, parse the JSON content. Only proceed with files where the top-level key `"status"` has the exact value `"archivable"`. Ignore files where `"status"` is `"active"` or missing.

3. **Large-scale Text Editing**:
   Modify the eligible JSON files in-place. Change the `"status"` value from `"archivable"` to `"archived"`. Ensure the files remain valid JSON.

4. **Archive Creation & Cleanup**:
   Create a compressed tarball at `/home/user/cold_storage.tar.gz` containing only the modified JSON files. The paths inside the tarball should be relative to `/home/user/data_volume` (e.g., `dirA/record_1.json`). 
   After successfully adding them to the archive, delete the archived JSON files from the active `/home/user/data_volume`. Do not delete the directories.

5. **Reporting**:
   Generate a CSV report at `/home/user/archive_report.csv` listing all the files you archived.
   The CSV must have the exact header: `filepath,new_status`
   The `filepath` must be the relative path from `/home/user/data_volume` (e.g., `dirA/record_1.json`).
   The `new_status` must be `archived`.
   Sort the CSV rows (excluding the header) alphabetically by `filepath`.

Ensure your script handles paths with spaces or special characters safely.