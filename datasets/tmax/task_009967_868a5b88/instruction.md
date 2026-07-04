You are a storage administrator managing disk space on a heavily utilized server. A custom backup system writes data to the `/home/user/storage_pool/` directory, distributing files across various subdirectories. Recently, there was a disk write error, and some of the backup archive files have become corrupted. You need to identify all corrupted files so they can be deleted to reclaim space.

All valid backup files (which may have any extension or no extension) in this directory must conform to a custom binary format:
1. **Magic Number:** The first 4 bytes must be `0x42 0x4B 0x55 0x50` (which corresponds to the ASCII string `BKUP`).
2. **Size Header:** The next 4 bytes (bytes 4-7) are an unsigned 32-bit integer in little-endian format representing the exact size of the payload in bytes.
3. **Payload:** The rest of the file (starting at byte 8) is the payload. The actual size of the payload MUST exactly match the size specified in the size header.

If a file lacks the correct magic number, has a truncated header, or its payload size does not match the size header exactly, it is considered corrupted.

**Your Task:**
1. Write a C program at `/home/user/validator.c` that takes a single file path as a command-line argument. The program should evaluate the specified file against the rules above. It should exit with code `0` if the file is valid, and exit with code `1` if the file is corrupted or cannot be read.
2. Compile this program to `/home/user/validator`.
3. Use your compiled program along with standard Linux shell commands to recursively traverse `/home/user/storage_pool/` and check every file.
4. Output the absolute paths of all corrupted files to `/home/user/corrupted_files.txt`. Ensure the paths are written one per line, and the final file is sorted alphabetically.