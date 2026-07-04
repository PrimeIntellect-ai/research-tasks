You are acting as a storage administrator managing disk space. We have an old backup system that uses a custom Run-Length Encoding (RLE) compression format. Disk space is running low because many of these archives decompress to the exact same file content. 

Your task is to write and execute a C++ program (`/home/user/storage_optimizer.cpp`) that performs custom decompression, archive verification, and file deduplication using hard links.

Here are the specific requirements:

1. **Configuration File Interpretation**:
   Read the configuration file at `/home/user/config.txt`. It contains key-value pairs (one per line, separated by `=`). You need to extract two values:
   - `ARCHIVE_DIR`: The directory containing the compressed files.
   - `MAGIC_HEADER`: The string that must appear on the first line of a valid archive.

2. **Archive Verification & Custom Decompression**:
   Iterate through all `.rle` files in the `ARCHIVE_DIR`. 
   - Check the first line of each file. If it does not exactly match the `MAGIC_HEADER`, skip the file (it is corrupt or a different version).
   - If it matches, decompress the second line of the file. The custom RLE format consists of integer counts followed immediately by a single character (e.g., `3A2B` decompresses to `AAABB`).
   - Save the decompressed string to a new file in the same directory, using the original filename but changing the `.rle` extension to `.txt` (e.g., `backup1.rle` becomes `backup1.txt`).

3. **Disk Space Optimization (Hard Linking)**:
   After extracting all valid `.txt` files, find files that have identical content. 
   - Keep the alphabetically first file (e.g., `backup1.txt` comes before `backup2.txt`) as the original.
   - Replace any other `.txt` files that have identical content with a hard link to the original `.txt` file.

4. **Logging**:
   Create a log file at `/home/user/link_count.log` that contains a single integer representing the total number of duplicate `.txt` files that were replaced with hard links.

Compile your C++ code and run it to process the backups. Ensure all file operations, deduplications, and the final log file are generated correctly.