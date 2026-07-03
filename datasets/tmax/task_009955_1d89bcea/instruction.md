You are a storage administrator managing a legacy data volume. You have discovered a backup directory at `/home/user/storage_data` that contains archived files. Due to a messy migration, this directory contains symbolic links to other directories (some of which point outside the main tree, and some of which form infinite loops).

Your task is to extract data from all uniquely reachable archive files without getting stuck in infinite symlink loops.

The archived files all have the `.zxt` extension. They are compressed using a custom Run-Length Encoding (RLE) and contain text encoded in UTF-16LE. 
The custom `.zxt` binary format is defined as a sequence of 3-byte chunks:
- Byte 1: An unsigned 8-bit integer representing the repetition count (1 to 255).
- Bytes 2-3: A 16-bit character in UTF-16LE encoding.
For example, the byte sequence `03 41 00` means the character 'A' (U+0041) repeated 3 times.

Perform the following steps:
1. Write a C program at `/home/user/decompress.c` that reads this custom `.zxt` binary format from standard input, decompresses it, converts the UTF-16LE characters to standard UTF-8, and prints the result to standard output. Compile it to `/home/user/decompress`.
2. Write a bash script or use shell commands to recursively traverse `/home/user/storage_data`. 
3. You MUST follow symbolic links to discover files, but you must implement a mechanism to avoid infinite loops and ensure that each physical `.zxt` file is processed exactly once (even if multiple symlinks point to it).
4. For every unique `.zxt` file discovered, decompress and decode it using your C program.
5. Generate a report at `/home/user/summary.log`. Each line should be formatted exactly as:
`<absolute_resolved_path_of_file>: <decoded_utf8_string>`
6. The lines in `/home/user/summary.log` must be sorted alphabetically by the absolute resolved path.

Ensure your C program gracefully handles standard EOF. Do not use any external libraries in your C code other than the standard C library (e.g., `<stdio.h>`, `<stdint.h>`).