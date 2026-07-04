You are an AI assistant helping a C developer organize a messy build directory. 

The developer has a directory at `/home/user/project/artifacts` containing several files with arbitrary names (e.g., `blobA`, `blobB`). These files are a mix of compiled C executables, C object files (relocatable), and plain text files.

Your task is to organize and process these files using shell commands:

1. Create a directory called `/home/user/project/organized/`.
2. Inspect the binary format of each file in `/home/user/project/artifacts`. 
3. Based on the file type, copy the valid ELF files into `/home/user/project/organized/` and rename them according to the following bulk-renaming rules:
   - If the file is an **ELF executable**, rename it to `exe_<original_name>.bin`
   - If the file is an **ELF relocatable** (object file), rename it to `obj_<original_name>.o`
   - Ignore any non-ELF files (do not copy them).
4. Create a directory called `/home/user/project/chunks/`.
5. Find the largest executable file (the largest `.bin` file) in the `/home/user/project/organized/` directory.
6. Split this largest executable into exactly 1024-byte (1KB) chunks, saving the chunks in `/home/user/project/chunks/`. The chunks must be named with the prefix `part_` and a two-letter suffix (e.g., `part_aa`, `part_ab`, `part_ac`).

Do not use any external scripts; standard bash built-ins and coreutils (`file`, `cp`, `split`, etc.) are fully sufficient.