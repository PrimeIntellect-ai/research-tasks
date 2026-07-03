You are a storage administrator managing a massive disk space cleanup. A faulty backup script previously ran amok, creating recursive symlinks and leaving thousands of awkwardly named backup files scattered across the system. 

Your tasks are to clean up the directory, fix a damaged manifest indexer, and generate a final report:

1. **Navigation & Cleanup**: 
   Navigate to `/home/user/storage_pool`. There is a symlink in this tree that points back to its own parent directory, causing an infinite loop. Find and delete ONLY this recursive symlink.

2. **Bulk Renaming**: 
   Recursively find all files ending in `.cpp.old_backup` inside `/home/user/storage_pool` and its subdirectories. Rename them so they end in `.cpp` instead.

3. **Text Transformation**: 
   Inside all the newly renamed `.cpp` files, use `sed` (or a similar tool) to replace every occurrence of the exact string `// TODO: STORAGE_QUOTA` with `// QUOTA_CHECKED`.

4. **Manifest Generation**: 
   Generate a checksum manifest file at `/home/user/manifest.txt`. The manifest must contain the SHA-256 hashes of all `.cpp` files in `/home/user/storage_pool` (and its subdirectories). 
   Format the file exactly like the standard output of `sha256sum` (e.g., `<hash>  <absolute_path_to_file>`), and sort the lines alphabetically by the file path.

5. **C++ Compilation and File Locking**:
   There is a program at `/home/user/indexer.cpp` designed to parse your manifest, safely acquire an exclusive file lock, and write the final count to `/home/user/storage_report.log`.
   However, the previous admin left a compilation error in the file (missing the correct header for `flock`).
   Fix the C++ file, compile it using `g++ /home/user/indexer.cpp -o /home/user/indexer`, and run it by passing the manifest path: `/home/user/indexer /home/user/manifest.txt`.

Verification:
An automated test will check that:
- The infinite symlink is removed.
- All `.cpp` files have the correct contents and names.
- `/home/user/manifest.txt` is perfectly formatted and sorted.
- `/home/user/storage_report.log` exists, contains the correct final output, and was written using the fixed C++ program.