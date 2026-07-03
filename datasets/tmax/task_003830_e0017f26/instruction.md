You are helping a technical writer organize and back up a massive, complex documentation repository. The writer uses a custom-built, Python-based archiving workflow, relying on the `fs` (PyFileSystem2) library. However, the system has been failing recently due to an infinite loop caused by symlinks.

Here are your objectives:

1. **Fix the Vendored Filesystem Library:**
   We have vendored the `fs` (PyFileSystem2) library source code at `/app/fs`. A recent internal modification to `fs/osfs.py` introduced a bug: it blindly follows symlinks during directory traversal, which causes an infinite recursion crash when hitting circular symlinks.
   - Locate the perturbation in `/app/fs/fs/osfs.py` (specifically around how directory entries are evaluated for `is_link` or similar checks during traversal) and fix it so that symlinks are treated safely or skipped entirely during recursive operations.
   - Install the fixed package into your Python environment.

2. **Safely Copy the Documentation Repository:**
   The documentation repository is located at `/home/user/docs`. It contains nested directories and a problematic circular symlink.
   - Write a Python script at `/home/user/backup_docs.py` that imports `fs.copy` and uses `fs.copy.copy_fs('osfs:///home/user/docs', 'osfs:///home/user/backup_staging')` to copy the repository.
   - Run the script. If you fixed the library correctly, it will safely copy the files without entering an infinite loop.

3. **Process the Large Metadata File using Memory-Mapped I/O:**
   The documentation system generated a large binary metadata file at `/home/user/metadata.bin`. We need to extract the starting byte offsets of every documentation section marker.
   - Write a script at `/home/user/process_meta.py`.
   - Using memory-mapped I/O (`mmap` module), efficiently search `/home/user/metadata.bin` for all occurrences of the exact 8-byte sequence: `b'DOC_MARK'`.
   - Write the integer byte offsets of every occurrence to `/home/user/offsets.txt`, with each offset on a new line, in ascending order.

Ensure all scripts execute successfully and `/home/user/offsets.txt` is perfectly accurate.