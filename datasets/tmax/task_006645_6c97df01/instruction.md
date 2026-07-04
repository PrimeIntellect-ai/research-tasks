You are a backup administrator tasked with archiving an active directory of logs using a custom compression scheme before standard zipping. 

We need you to write a custom C program that navigates a directory tree, reads log files, applies a specific Run-Length Encoding (RLE) to the data stream, and outputs the result so it can be piped into standard compression tools.

Your task has three phases:
1. **Write the Custom Archiver (`/home/user/compress_logs.c`)**
   Write a C program that accepts a single directory path as a command-line argument.
   - It must recursively navigate the directory and find all files ending in `.log`.
   - It must sort the absolute file paths alphabetically (lexicographically) before processing them to ensure a deterministic output order.
   - For each `.log` file, print the absolute file path on a single line, ending with a newline `\n`.
   - Then, read the file character by character and apply a custom RLE, printing directly to standard output (`stdout`).
   - **RLE Rules:**
     - For ALL characters EXCEPT the newline character (`\n`), count consecutive identical characters.
     - The maximum run length is 9. If a character appears 10 times consecutively, it should be output as a run of 9, followed by a run of 1.
     - The output format for compressed characters is `[count][character]`. (e.g., `aaa` becomes `3a`, `          ` (10 spaces) becomes `9 1 `).
     - Newline characters (`\n`) must NOT be compressed or counted. When you encounter a `\n`, simply output `\n` as-is.
     - Do not add any extra newlines between files; only output what is dictated by the rules above and the file contents.

2. **Compile and Execute**
   - Compile your program to `/home/user/compress_logs`.
   - Run the program against the `/home/user/active_logs` directory.
   - Redirect and pipe its standard output into `gzip`, saving the final compressed archive to `/home/user/archive.rle.gz`.

3. **Verify Archive Integrity**
   - To prove the pipeline worked, decompress the `archive.rle.gz` stream on the fly (using `zcat` or similar) and pipe it to `md5sum`.
   - Save the resulting MD5 checksum (just the hash string, no file paths or hyphens) to `/home/user/archive_checksum.txt`.

Ensure your C program handles standard POSIX directory traversal (e.g., using `dirent.h`) and standard I/O properly.