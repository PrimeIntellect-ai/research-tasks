You are tasked with fixing a broken configuration backup system. The configuration directory `/home/user/config_tree` contains various application settings, but a bug in a previous automation script created several symlinks that resolve to infinite loops. Standard backup tools are failing or getting stuck when trying to follow these links.

Your objective is to write a C program that sanitizes this directory, logs the issues, and creates a safe, compressed backup.

Write a C program at `/home/user/safe_backup.c` that performs the following steps when executed:

1. **Traversal and Loop Detection**: Recursively traverse the `/home/user/config_tree` directory. Identify any symlinks that result in an infinite loop (i.e., attempting to resolve their absolute path fails due to too many symbolic links).
2. **Bulk Renaming**: When a looping symlink is detected, rename it by appending `.broken` to its filename (e.g., `bad_link` becomes `bad_link.broken`). Do not delete the link. Do not modify valid symlinks or regular files.
3. **Logging**: Whenever a looping symlink is renamed, append its original absolute path to `/home/user/broken_links.log`. Each path must be on a new line.
4. **Atomic Archive Creation**: After the directory is sanitized, the C program must create a gzip-compressed tar archive of the entire `/home/user/config_tree` directory. To prevent incomplete backups from being read by concurrent processes, this must be done atomically:
   - First, create the archive at the temporary path `/home/user/config_backup.tar.gz.tmp`.
   - Once the archive is completely written and the archiving process exits successfully, atomically rename the temporary file to its final destination: `/home/user/config_backup.tar.gz`.

**Requirements**:
- The program must be written in C. You may use standard libraries and POSIX APIs (like `realpath`, `rename`, `opendir`, `lstat`, etc.).
- You may use `system()`, `popen()`, or `fork()`/`exec()` to invoke external tools (like `tar`) for the compression step.
- The final archive must contain the contents of `/home/user/config_tree` (including the newly renamed `.broken` links).
- Ensure your code compiles without warnings using standard `gcc`. You do not need to compile or run the program yourself; the evaluation environment will compile `/home/user/safe_backup.c` and execute it to verify the results.