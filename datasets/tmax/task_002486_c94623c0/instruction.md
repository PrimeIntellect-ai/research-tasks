You are acting as a backup administrator archiving custom data. We have a primary storage directory at `/home/user/data/` containing various proprietary archive files (with `.arc` extensions) along with other miscellaneous files.

Your task is to perform a custom incremental backup and generate a manifest of the backed-up files. Specifically, you must:

1. **Metadata-based File Search:** Find all `.arc` files in `/home/user/data/` that are larger than 10 KB and have been modified within the last 7 days.
2. **Binary Header Extraction:** Write a C program at `/home/user/get_header.c` and compile it to `/home/user/get_header`. The program must take a single command-line argument (the file path), open the file in binary mode, read exactly the first 8 bytes, and print them to standard output as uppercase hexadecimal numbers separated by a single space (e.g., `DE AD BE EF 00 00 00 01`), followed by a newline.
3. **Manifest Generation & Path Manipulation:** Using the files found in step 1 and your C program, generate a backup manifest file at `/home/user/manifest.txt`. For each matching file, the manifest should contain a line formatted exactly like this:
   `[8-BYTE HEX HEADER] /vault/archive/<filename>`
   *(Note: You must transform the original path `/home/user/data/<filename>` to the new destination path `/vault/archive/<filename>` in the manifest text).* 
   Sort the lines in `/home/user/manifest.txt` alphabetically by the file name.
4. **Incremental Backup:** Create an uncompressed tar archive at `/home/user/inc_backup.tar` containing only the files identified in step 1. Store them in the tar archive using their relative paths from `/home/user/data/` (i.e., the tarball should contain `file1.arc`, not `home/user/data/file1.arc`).

Ensure all outputs strictly match the required formats, as they will be automatically verified.