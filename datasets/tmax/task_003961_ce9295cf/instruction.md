I am reorganizing some project files and need to sanitize and archive a large log file. I have a monolithic log file located at `/home/user/project_logs.txt`. 

Please write and execute a Rust program (save the source at `/home/user/process_logs.rs`) that performs the following tasks:

1. **Text Editing / Sanitization:** Read the entire `/home/user/project_logs.txt` file. Find all instances matching the pattern `API_KEY=` followed by any alphanumeric characters (e.g., `API_KEY=abc123`) and replace the alphanumeric part with `REDACTED` (so it becomes `API_KEY=REDACTED`).
2. **File Chunking:** Split the sanitized log data into smaller files of exactly 50 lines each. Save these files in a new directory called `/home/user/chunks/`. Name the files sequentially starting from 1: `part_1.txt`, `part_2.txt`, `part_3.txt`, etc.
3. **Symbolic Link Management:** Create a new directory called `/home/user/symlinks/`. For every **even-numbered** chunk (e.g., `part_2.txt`, `part_4.txt`), create a symbolic link in the `/home/user/symlinks/` directory pointing to the chunk file. The symlink should be named `active_N.txt` where N is the even number (e.g., `active_2.txt` pointing to `../chunks/part_2.txt`). The symlink target must be a relative path.
4. **Archiving:** After the chunks and symlinks are created, use standard Linux shell commands to compress the entire `/home/user/chunks/` directory into a tarball named `/home/user/clean_logs.tar.gz`.

Ensure your Rust code compiles and runs successfully, and the final `.tar.gz` and symlinks are exactly where specified. Do not delete the original `project_logs.txt` file.