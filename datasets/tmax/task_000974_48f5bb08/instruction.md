I am a technical writer organizing a large documentation repository. Recently, my automated backup script went haywire because it blindly followed a circular symlink (`/docs/shared/shared/shared/...`), resulting in an infinitely growing, corrupted backup archive before the process was killed.

The backup file is located at `/home/user/backup.bin`. It was created using a custom binary archiver. I need you to write a C++ program that can read this archive from standard input, safely extract the valid documentation files, stop when it detects the infinite loop, and log the recovered files using POSIX file locking.

Here is the specification for the custom binary format:
Every file in the archive consists of a 128-byte header followed immediately by the file data.
The header format is:
- Bytes 0-99: The relative file path as a null-terminated ASCII string (e.g., `intro.md`). If the path is shorter than 100 bytes, the rest are null bytes (`\0`).
- Bytes 100-107: An unsigned 64-bit integer (little-endian) representing the file size in bytes.
- Bytes 108-127: Reserved (can be ignored).

Your C++ program (`/home/user/recover.cpp`) must:
1. Read the binary data from standard input (`std::cin`).
2. Parse the headers and extract the files into the directory `/home/user/recovered_docs/` (create this directory if it doesn't exist).
3. To handle the infinite loop, you must inspect each file path. If the path contains the string `"shared/shared/` anywhere in it, you have reached the start of the corrupted loop. Stop parsing the archive immediately and exit gracefully. Do NOT extract this file or any subsequent files.
4. For every file successfully extracted, append its path and size to a log file at `/home/user/recovery.log`. The format should be exactly `[path]: [size] bytes\n`.
5. Because this recovery might be run concurrently by different workers in the future, you must use POSIX file locking (`fcntl` or `flock` with exclusive lock `F_WRLCK` or `LOCK_EX`) on `recovery.log` while writing to it. Unlock it after writing.

Once your C++ code is written and compiled, run it by piping the backup file into it:
`cat /home/user/backup.bin | /home/user/recover`

Please ensure your C++ code handles binary streams correctly and securely creates directories as needed (you can use `std::filesystem` for directory creation).