I am a researcher trying to organize my experimental datasets in `/home/user/datasets`. Unfortunately, a previous automated script went rogue and created several infinite symlink loops within the directory structure. 

I need you to write a C program that can safely traverse this directory, identify the loops, and compress the valid data files.

Please write a C program at `/home/user/clean_backup.c` that does the following:
1. Recursively traverses the `/home/user/datasets` directory.
2. Follows directory symlinks, but keeps track of visited directory inodes in the current traversal branch to detect infinite loops. 
3. If a symlink points to a directory that causes an infinite loop (i.e., its target inode is already in the current branch's stack), log the absolute path of that offending symlink to `/home/user/loop_report.txt` (one path per line) and do not follow it.
4. For every regular file encountered that has the `.dat` extension, use the `zlib` library (e.g., `gzopen`, `gzwrite`) to compress it. Save the compressed file to the existing directory `/home/user/compressed/`. The output file should be named `<original_filename>_<inode>.gz` (where `<inode>` is the inode number of the `.dat` file). Do not follow symlinks to files, only process regular `.dat` files.

After writing the code:
1. Compile it using `gcc -o /home/user/clean_backup /home/user/clean_backup.c -lz`.
2. Run the executable.
3. Verify the integrity of all generated `.gz` archives in `/home/user/compressed/` using the standard `gzip -t` command.

The `/home/user/compressed/` directory already exists. Make sure your C code handles absolute paths correctly and gracefully skips any permissions errors if encountered.