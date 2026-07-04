You are an AI assistant helping to secure a configuration management system. We process uncompressed configuration archives (`.tar` files) sent by external nodes, but we suspect some of them are attempting "Zip Slip" directory traversal attacks to overwrite sensitive files.

Your task is to write a C program that safely inspects an incoming tarball and flags malicious paths without extracting them. Additionally, the configuration manager expects certain safe payloads to be ELF executables, so you must also identify valid, safe ELF files within the archive.

Input file: `/home/user/config_update.tar`

Write a C program at `/home/user/analyze.c` that reads `config_update.tar` directly (parsing the binary tar structure) and does the following:

1. Iterates through the files in the uncompressed tar archive.
   *Hint: In a standard POSIX tar file, each file has a 512-byte header block. The file name is in the first 100 bytes (null-terminated). The file size is stored at offset 124 as an octal string (12 bytes). The file data immediately follows the header, padded with null bytes to a multiple of 512 bytes.*
2. Checks the filename for directory traversal attempts. A file is considered malicious if its path starts with `/` or contains the substring `../`.
3. If the file is malicious, append its exact filename to `/home/user/alerts.log`.
4. If the file is NOT malicious, check its payload (the actual file contents inside the tar). If the first 4 bytes of the payload are the ELF magic number (`\x7F` followed by `ELF`), append its exact filename to `/home/user/safe_elfs.log`.

Constraints:
- Do not use external libraries (like libtar) or shell out to the `tar` command in your C code. Read the binary format directly using standard C file I/O (`fread`, `fseek`, etc.).
- Ensure your output log files are sorted alphabetically if you process them further, or simply written in the order they appear in the archive. (Writing in the order they appear in the archive is perfectly fine).
- Compile your program using `gcc /home/user/analyze.c -o /home/user/analyze` and run it.

Please verify your solution by ensuring `/home/user/alerts.log` and `/home/user/safe_elfs.log` contain the correct filenames separated by newlines.