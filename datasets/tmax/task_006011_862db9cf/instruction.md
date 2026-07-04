You are a backup administrator tasked with creating a custom incremental archiving solution for a sensitive dataset. Your goal is to build a fast, lightweight backup utility in C that compresses individual files and appends them to a single custom binary archive, along with a bash script to manage incremental backups.

**Part 1: The C Archiver (`/home/user/compress_append.c`)**
Write a C program that takes exactly two arguments: an input file path and an archive file path. 
Example usage: `./compress_append /home/user/data/report.txt /home/user/archive.dat`

The program must perform the following operations:
1. Open the input file and read its entire contents.
2. Compress the contents using the standard `zlib` library (specifically the `compress()` function).
3. Open the archive file in append mode. If it does not exist, create it.
4. Append a custom header and the compressed payload in the following exact binary format:
   - **Filename Length (1 byte):** An unsigned 8-bit integer representing the length of the *basename* of the input file (e.g., "report.txt" has length 10).
   - **Filename (N bytes):** The exact basename string (do not include the null terminator).
   - **Compressed Payload Size (4 bytes):** An unsigned 32-bit integer representing the size of the *compressed* data, written in little-endian format.
   - **Compressed Data:** The raw bytes produced by zlib.
5. Close all file handles cleanly.

Compile this program to the executable `/home/user/compress_append`. Assume `gcc` and `zlib1g-dev` are already installed on the system. Compile it linking the zlib library (`-lz`).

**Part 2: The Incremental Backup Script (`/home/user/backup.sh`)**
Write a bash script to automate incremental backups of all `.txt` files located in `/home/user/data`.
The script must:
1. Look for a state file at `/home/user/backup.stamp`.
2. Find all `.txt` files in `/home/user/data` that are newer than `/home/user/backup.stamp`. If `/home/user/backup.stamp` does not exist, it should process all `.txt` files in the directory.
3. For each file found, invoke your `./compress_append` program to append it to `/home/user/master_archive.dat`.
4. After successfully processing the files, update (or create) `/home/user/backup.stamp` to the current time using the `touch` command.

**Part 3: Execution Steps**
To complete the task:
1. Ensure the C code and bash script are written and the C code is compiled.
2. Run your `/home/user/backup.sh` script once. It should back up the initial files present in `/home/user/data`.
3. Modify `/home/user/data/alpha.txt` by appending the exact line: `[MODIFIED] Additional data appended.`
4. Run your `/home/user/backup.sh` script a second time. It should detect the modification and append *only* `alpha.txt` to `/home/user/master_archive.dat`.

Your final output will be verified by programmatically inspecting the structure and uncompressed contents of `/home/user/master_archive.dat`.