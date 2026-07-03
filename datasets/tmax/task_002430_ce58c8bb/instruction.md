You are a configuration manager tracking changes in an old system. You have received an archive of unidentified binary blobs that contain system plugins and database transaction logs.

Your task is to identify and process these files. 

1. Extract the archive located at `/home/user/configs.tar.gz` into the directory `/home/user/configs/`.
2. Write a C program `/home/user/process_configs.c` (and compile it to `/home/user/process_configs`) that iterates over all regular files in `/home/user/configs/` and does the following:
   - Reads the first 4 bytes of each file to determine its type.
   - If the file starts with the standard ELF magic number (`0x7F` followed by `ELF`), rename it by appending the `.elf` extension (e.g., `blob1` becomes `blob1.elf`).
   - If the file starts with the SQLite WAL (Write-Ahead Log) magic number (`0x37 0x7F 0x06 0x82` or `0x37 0x7F 0x06 0x83`), rename it by appending the `.wal` extension.
   - If the file is neither an ELF nor a WAL file, delete it from the directory.
3. Run your compiled C program.
4. Finally, create a new gzip-compressed tar archive at `/home/user/updated_configs.tar.gz` that contains ONLY the newly renamed `.elf` and `.wal` files. Do not include the `/home/user/configs/` directory itself in the tarball paths (the files should be at the root of the archive).

Ensure that your C program directly handles the file opening, reading, renaming, and deletion (using standard C library functions like `fopen`, `fread`, `rename`, `remove`). You can use bash commands for extraction, compilation, and creating the final archive.