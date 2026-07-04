You are acting as a backup administrator archiving legacy application data. You have a directory of recovered binary blobs and documentation that need to be organized, analyzed, and deduplicated before moving them to cold storage.

The recovered files are located in `/home/user/bin_backup`. There are several `.bin` files, some of which are ELF executables (32-bit or 64-bit) and some of which are raw data. There is also a documentation file `readme.txt` that was recovered from an old Windows system and is encoded in UTF-16LE.

Your task is to complete the following steps:

1. **Domain-Specific Parsing (C Language):**
   Write a C program at `/home/user/elf_checker.c` and compile it to `/home/user/elf_checker`. The program must take a single file path as a command-line argument. It should open the file, read the first 5 bytes (the ELF header), and check if it is a valid ELF file (`\x7F E L F`). If it is, check the 5th byte (the architecture class). 
   - Print `32` if it is a 32-bit ELF.
   - Print `64` if it is a 64-bit ELF.
   - Print `UNKNOWN` if it is not an ELF file or the file cannot be opened.
   Ensure the program prints only this string and a newline.

2. **Bulk Renaming:**
   Using your compiled `elf_checker`, loop through all `.bin` files in `/home/user/bin_backup`. Rename each file to include its detected architecture just before the extension. 
   For example, `app.bin` should become `app_32.bin`, `app_64.bin`, or `app_UNKNOWN.bin`.

3. **Link Management:**
   Create the directories `/home/user/bin_archive/32` and `/home/user/bin_archive/64`.
   - For every 32-bit binary you renamed, create a **symbolic link** in `/home/user/bin_archive/32/` pointing to the renamed file in `/home/user/bin_backup/`.
   - For every 64-bit binary you renamed, create a **hard link** in `/home/user/bin_archive/64/` pointing to the renamed file.

4. **Character Encoding Conversion:**
   Convert the encoding of `/home/user/bin_backup/readme.txt` from UTF-16LE to UTF-8, and save the converted output as `/home/user/bin_backup/readme_utf8.txt`.