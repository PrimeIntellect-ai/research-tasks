You are tasked with organizing and verifying a set of archived C project files for a legacy codebase. The project files were recovered from a potentially corrupted archive, and you must verify their integrity, safely log the valid files, and then apply a codebase-wide macro update.

Here are the requirements:

1. **Extraction**: Extract the archive located at `/home/user/project.tar` into the directory `/home/user/src/`. Create the directory if it does not exist.

2. **Integrity Verification and Logging (C Program)**:
   Write a C program at `/home/user/verify.c` and compile it to `/home/user/verify`. This program must:
   - Open and read the binary index file `/home/user/hashes.bin` using **memory-mapped I/O (`mmap`)**. 
   - The `hashes.bin` file contains an array of 32-byte records. Each record consists of:
     - `char filename[31]` (null-terminated string representing the filename)
     - `uint8_t checksum` (an 8-bit XOR sum of the file's original contents)
   - For each record found in `hashes.bin`, your program should read the corresponding extracted file from `/home/user/src/` and compute its 8-bit XOR checksum (initialize a `uint8_t` to `0`, then XOR it with every byte of the file).
   - If a file's computed checksum matches the checksum in `hashes.bin`, the file is intact.
   - For every intact file, append its filename (e.g., `main.c`) followed by a newline to `/home/user/verified.log`.
   - **Crucial**: Because this program is designed to be run in a concurrent pipeline, it *must* acquire an exclusive file lock (using `flock()` or `fcntl()`) on `/home/user/verified.log` before writing, and release it after writing.

3. **Macro Application (Text Editing)**:
   After running your C program to populate `/home/user/verified.log`, you must update the legacy codebase. For *only* the files successfully listed in `/home/user/verified.log`, replace every occurrence of the string `DEPRECATED_API_CALL` with `MODERN_API_CALL`. You can use shell commands/tools (like `sed`, `awk`, or `xargs`) for this step. Do not modify files that failed the integrity check.

**Starting State:**
- `/home/user/project.tar` exists and contains several `.c` files.
- `/home/user/hashes.bin` exists.

**Success Criteria:**
- `/home/user/verify.c` compiles and uses `mmap` and file locking.
- `/home/user/verified.log` contains only the names of the files that passed the integrity check.
- The valid files in `/home/user/src/` have `MODERN_API_CALL` instead of `DEPRECATED_API_CALL`.
- The corrupted files remain unmodified.