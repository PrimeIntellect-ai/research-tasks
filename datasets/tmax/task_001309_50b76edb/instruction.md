You are acting as a storage administrator. We are running out of disk space on our server and need to optimize our storage and analyze some critical logs. 

All files are located in `/home/user/storage_dump`.

Please complete the following objectives:

1. **Deduplication (Hard Links)**: Traverse the `/home/user/storage_dump` directory recursively. Find all regular files that have identical content. Keep one instance of each unique file, and replace all its other identical copies with a **hard link** to the kept instance. This will free up disk space without changing the directory structure or file names.

2. **Multi-part Archive Reassembly and Symlinking**: In `/home/user/storage_dump/archives/`, there is a split multi-part archive named `system_backup.tar.gz.001`, `system_backup.tar.gz.002`, etc. 
   - Recombine these parts in order.
   - Extract the resulting archive into `/home/user/extracted_backup/` (create the directory if it doesn't exist).
   - Create a symbolic link at `/home/user/latest_backup` that points to the `/home/user/extracted_backup/` directory.

3. **Multi-line Log Parsing**: Traverse `/home/user/storage_dump/` to find all files ending with `.log`. Extract all multi-line error blocks that begin with `[CRITICAL_START]` and end with `[CRITICAL_END]` (inclusive). Redirect and append all extracted blocks into a single file at `/home/user/critical_errors.txt`. Ensure the output only contains the lines within these blocks.

You can use any language or shell commands you prefer to accomplish these tasks.