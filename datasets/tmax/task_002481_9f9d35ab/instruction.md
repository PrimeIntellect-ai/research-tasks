You are an AI assistant acting as a storage administrator. You need to write a C program that helps manage disk space by automatically deduplicating files using hard links and organizing them using symbolic links.

Your task is to write and compile a C program named `/home/user/storage_dedup.c` to an executable `/home/user/storage_dedup`. 

The program must do the following:
1. **Configuration Interpretation**: On startup, read a text configuration file at `/home/user/config.txt`. It will contain exactly two lines:
   `WATCH_DIR=/path/to/watch`
   `ARCHIVE_DIR=/path/to/archive`
   (Note: Extract the actual paths after the `=` sign).

2. **File Watching**: Use Linux `inotify` to continuously monitor the `WATCH_DIR` for `IN_CLOSE_WRITE` events (files that have been written to and closed). 

3. **Binary Comparison and Link Management**: 
   When a new file triggers the event in `WATCH_DIR`:
   - Open and read the new file in binary mode.
   - Iterate through all regular files currently in the `ARCHIVE_DIR`.
   - Compare the binary contents of the new file against the files in `ARCHIVE_DIR`.
   - **If an exact binary match is found** in `ARCHIVE_DIR` (e.g., `ARCHIVE_DIR/existing.dat`):
     - Delete the newly written file in `WATCH_DIR`.
     - Create a **hard link** in `WATCH_DIR` with the exact same name as the deleted file, pointing to the matched file in `ARCHIVE_DIR`.
     - Append a line to `/home/user/dedup.log`: `DUPLICATE: <filename> -> <matched_archive_file>` (where filename is just the basename, e.g., `file1.bin -> existing.dat`).
   - **If no exact match is found**:
     - Move the newly written file from `WATCH_DIR` to `ARCHIVE_DIR`, keeping its original basename.
     - Create a **symbolic link** in `WATCH_DIR` with the same basename, pointing to the newly moved file in `ARCHIVE_DIR`. The symlink should use the absolute path to the archive file.
     - Append a line to `/home/user/dedup.log`: `NEW: <filename> -> <filename>`

**Constraints and requirements**:
- The program should run in an infinite loop waiting for `inotify` events until terminated.
- Do not process directories, only regular files.
- Compile your program with `gcc /home/user/storage_dedup.c -o /home/user/storage_dedup`.
- Ensure the executable is present at `/home/user/storage_dedup`. You do not need to leave the program running; the automated test will execute it, drop files into the watch directory, and inspect the resulting filesystem state and `/home/user/dedup.log`.