You are tasked with maintaining an artifact repository. Our system curates binary files and archives them, but recent updates have introduced cyclic symlinks and concurrent locking issues. 

You must write a C program, `/home/user/curator.c`, and compile it to `/home/user/curator`. 
This program must do the following:
1. Recursively traverse the directory `/home/user/artifacts`.
2. For every file or symlink encountered (ignoring `.` and `..`), use `realpath()` or similar metadata checks to resolve its absolute path.
3. **Symlink Loop Detection:** If a file is a symlink that results in an infinite loop (e.g., resolving fails with `ELOOP`), append the line `LOOP_DETECTED: <absolute_path_of_symlink>` to `/home/user/curation.log`.
4. **File Locking and Concurrency:** For all valid, resolvable regular files (whether accessed directly or via a valid symlink), attempt to open the resolved file and acquire an exclusive, non-blocking POSIX record lock using `fcntl()` (`F_WRLCK` with `F_SETLK`). 
   - If the lock fails because another process holds it (returns `EAGAIN` or `EACCES`), append the line `LOCKED: <resolved_absolute_path>` to `/home/user/curation.log`.
   - If the lock succeeds, write the `resolved_absolute_path` to `/home/user/safe_artifacts.txt` (one path per line), remove the lock, and close the file.
   - Note: If multiple valid symlinks point to the same file, or you visit the file and its symlinks, process the resolved absolute path only once, or just attempt the lock each time (writing duplicates to the file is acceptable, we will handle deduplication later).

After writing and running your C program, use the output file `/home/user/safe_artifacts.txt` to create a compressed archive of the safe files.
Execute a shell command to read the paths in `/home/user/safe_artifacts.txt` and package them into a GZIP-compressed tarball located at `/home/user/safe_archive.tar.gz`. Ensure the files are stored with their absolute paths or appropriately archived so the test suite can verify the contents.

Requirements:
- Your C code must be robust and handle the standard filesystem headers (`<dirent.h>`, `<fcntl.h>`, `<unistd.h>`, etc.).
- Ensure both the C program and the shell command are fully executed before completing the task.