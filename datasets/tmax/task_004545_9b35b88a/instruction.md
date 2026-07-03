You are acting as a storage administrator. A runaway backup script has wreaked havoc on our backup storage server. The script attempted to archive files but improperly followed symlinks, resulting in infinite loops, deeply nested directories, and massive file duplication that is exhausting our disk space.

Your task is to write a Go program that untangles this mess by extracting unique files, avoiding symlink loops, and generating a verified manifest. 

The messy data is located at `/home/user/bloated_data/`.
A configuration file is provided at `/home/user/config.json`.

Write and execute a Go program (e.g., `/home/user/cleanup.go`) that performs the following steps:
1. **Read Configuration**: Parse `/home/user/config.json` which has the following structure:
   ```json
   {
     "source_dir": "/home/user/bloated_data",
     "dest_dir": "/home/user/cleaned_data",
     "manifest_path": "/home/user/manifest.json"
   }
   ```
2. **Safe Traversal & Deduplication**: Recursively walk the `source_dir`. 
   - **Crucial**: You must detect and completely ignore any symlinks to avoid infinite loops. Only process regular files.
   - Calculate the SHA256 checksum of every regular file.
   - To save disk space, deduplicate the files. If multiple files have the exact same contents (identical SHA256 hashes), only process the *first* one you encounter during the directory walk. Ignore subsequent duplicates.
3. **Bulk File Renaming & Copying**: 
   - Ensure the `dest_dir` exists (create it if it doesn't).
   - Copy each unique file into `dest_dir`. 
   - The new filename in `dest_dir` must be formatted as: `<first_8_chars_of_sha256>_<original_filename>`. (e.g., `a1b2c3d4_report.csv`).
4. **Manifest Generation**: 
   - Create a JSON manifest file at `manifest_path`.
   - The manifest must be an array of objects, each representing a uniquely copied file, sorted alphabetically by the `new_filename`.
   - Format of the manifest entries:
     ```json
     [
       {
         "original_path": "/home/user/bloated_data/path/to/report.csv",
         "new_filename": "a1b2c3d4_report.csv",
         "sha256": "a1b2c3d4e5f6..." 
       }
     ]
     ```

**Constraints & Verification:**
- You must use **Go** for the primary logic.
- Ensure the Go program compiles and runs successfully.
- Do not delete the original `/home/user/bloated_data/` directory.
- An automated test will read `/home/user/manifest.json` and verify the files in `/home/user/cleaned_data/`.