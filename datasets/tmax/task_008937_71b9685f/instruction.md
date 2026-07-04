You are an AI assistant helping a storage administrator manage disk space on a Linux server. There is a directory containing custom binary memory dump files at `/home/user/dumps`. Over time, this directory has grown too large, and we need to archive and remove older dumps.

The binary files (with a `.bin` extension) have a custom 16-byte header followed by a variable-length data payload. The header format is as follows (all values are little-endian):
- Bytes 0-3: Magic number `0xDEADBEEF` (unsigned 32-bit integer)
- Bytes 4-7: Unix timestamp representing when the dump was created (unsigned 32-bit integer)
- Bytes 8-15: Payload size in bytes (unsigned 64-bit integer)

Your task is to:
1. Write a C program at `/home/user/scanner.c` that scans the `/home/user/dumps` directory. For each `.bin` file, it must use memory-mapped I/O (`mmap`) to read the header, verify the magic number, and extract the timestamp.
2. The program must find all dump files with a timestamp strictly less than `1700000000`.
3. The C program should output the absolute paths of these "old" files, one per line, to a text file located at `/home/user/old_files.txt`.
4. Compile and run your program to generate `/home/user/old_files.txt`.
5. Using standard Linux utilities, read the `/home/user/old_files.txt` file and archive all the listed files into a single gzipped tarball located at `/home/user/old_dumps.tar.gz`. (The archive can store absolute or relative paths, as long as the file contents are preserved).
6. After successfully creating the archive, delete the original "old" `.bin` files from `/home/user/dumps` to free up disk space. Do not delete the files that have timestamps >= `1700000000`.

Requirements:
- You must write the parsing logic in C.
- You must use `mmap` for reading the files in your C code (standard `read()` is not allowed for the binary parsing).
- Ensure the final archive `/home/user/old_dumps.tar.gz` contains exactly the old files, and that those files no longer exist in `/home/user/dumps`.