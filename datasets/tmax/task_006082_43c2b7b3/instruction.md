As a storage administrator, you need to clean up an old backup server that is running out of disk space. A configuration file dictates where these backups are stored. Many of the backups are gzip-compressed files, and we suspect several of them are bulky 64-bit ELF executables that were accidentally archived. 

Write and execute a C++ program at `/home/user/scanner.cpp` (compiled to `/home/user/scanner`) that performs the following steps:

1. **Configuration file interpretation**: Read the file `/home/user/config.txt`. It contains a single line in the format `TargetDirectory=<path>`. Extract this path.
2. **Recursive directory traversal**: Recursively search the extracted `<path>` for all files ending in `.gz`.
3. **Compressed stream processing & Domain-specific format parsing**: For each `.gz` file found, determine if the compressed content is a 64-bit ELF binary. You can do this by inspecting the first 5 uncompressed bytes. A valid 64-bit ELF file starts with the magic sequence `0x7F 0x45 0x4C 0x46 0x02` (`\x7fELF\x02`). You may use standard C/C++ libraries or utilize `popen` to stream the uncompressed bytes via shell utilities like `zcat` or `gzip`.
4. **Log creation**: If a `.gz` file contains a 64-bit ELF binary, write its absolute path to a log file at `/home/user/to_delete.log`. Sort the paths alphabetically before writing them, so each path is on its own line.
5. **Archive creation**: After your C++ program finishes and successfully creates `/home/user/to_delete.log`, use a shell command to create an uncompressed tar archive named `/home/user/cleanup.tar` containing ONLY the `to_delete.log` file (do not include the full directory structure in the tar, just the file itself).

Ensure your C++ code handles errors gracefully and builds correctly with standard `g++`. Standard bash commands can be used to compile the code and create the final tar archive.