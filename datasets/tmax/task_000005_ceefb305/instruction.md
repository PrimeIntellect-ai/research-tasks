You are a backup administrator tasked with archiving active system binaries and legacy logs. You need to write a C program to safely extract metadata and convert log encodings, then use shell commands to create a multi-part archive.

Step 1: Write a C program
Create a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`. 
This program must do the following:
1. Open and acquire an exclusive file lock (`flock`) on a central metadata file located at `/home/user/archive_index.wal`. Create the file if it does not exist. The lock is required because in our real environment, multiple backup agents write to this file concurrently.
2. Read the legacy log file located at `/home/user/incoming/legacy_log.iso88591`. This file is encoded in `ISO-8859-1`. Convert its contents to `UTF-8` and write the converted text into `/home/user/archive_index.wal`.
3. Scan the `/home/user/incoming/` directory for 64-bit ELF executables. 
4. For every 64-bit ELF file found in that directory, parse its ELF header (using standard C structures like `Elf64_Ehdr`) to find the entry point virtual address (`e_entry`).
5. Append each discovered ELF entry point to `/home/user/archive_index.wal` in exactly this format, each on a new line:
   `ELF: <filename> ENTRY: 0x<hex_address>`
   (e.g., `ELF: prog1 ENTRY: 0x401050`)
6. Release the file lock and close `/home/user/archive_index.wal`.

Step 2: Create a multi-part archive
After running your C program, package both the `/home/user/incoming/` directory and the `/home/user/archive_index.wal` file into a compressed tarball (`.tar.gz`), and split it into multiple parts of exactly 1 Megabyte (1MB) each. 
Save these parts in the directory `/home/user/backup_parts/`.
Name the split files `backup.tar.gz.partaa`, `backup.tar.gz.partab`, etc.

Constraints:
- All file operations inside the C program must be written in C. Do not use `system()` calls to invoke shell tools like `iconv` or `readelf` from within the C code. Use native C libraries and headers (e.g., `<elf.h>`, `<iconv.h>`, `<sys/file.h>`).
- Compile your C program using `gcc /home/user/archiver.c -o /home/user/archiver`.
- Run your program before creating the archive.