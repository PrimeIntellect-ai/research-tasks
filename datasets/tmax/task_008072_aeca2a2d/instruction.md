You are an Artifact Manager responsible for curating our binary repositories. Over time, many binaries have become stale. We need a robust toolchain to perform incremental archives of these stale artifacts into a custom binary format.

Your task is to build a two-part archiving pipeline:

**Part 1: Manifest Filtering (`/home/user/find_stale.sh`)**
There is a manifest file located at `/home/user/artifacts/manifest.txt` with columns separated by spaces:
`ARTIFACT_ID  FILE_PATH  LAST_ACCESSED_DATE  STATUS`

Write a shell script at `/home/user/find_stale.sh` that uses text processing tools (like `awk` or `sed`) to parse this manifest and print *only* the `FILE_PATH` of artifacts to standard output if:
1. The `STATUS` is exactly `STALE`.
2. The file currently exists on the file system.

**Part 2: The Incremental Archiver (`/home/user/archiver.c`)**
Write a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`.
This program must read file paths from `stdin` (one per line) and incrementally archive them.

For each file path read from standard input:
1. Check if the exact file path is already listed in the index file `/home/user/archive_index.txt`. If it is, skip archiving this file.
2. If it is not in the index, open the file, read its contents, and append it to the binary archive `/home/user/stale_archive.bin`.
3. Append the processed file path to `/home/user/archive_index.txt` (followed by a newline).

**Archive Format Specifications:**
When appending a file to `/home/user/stale_archive.bin`, you must write exactly three components in order:
1. **Filename Header:** A 256-byte field containing the exact file path string. It must be null-terminated and the remaining bytes must be padded with null bytes (`\0`).
2. **Size Header:** An 8-byte unsigned integer (`uint64_t`) representing the file's size in bytes, encoded in **little-endian** byte order.
3. **Payload:** The raw binary bytes of the file itself.

**Execution:**
Once you have created both tools, run your pipeline:
`/home/user/find_stale.sh | /home/user/archiver`

Ensure all code compiles without standard library errors.