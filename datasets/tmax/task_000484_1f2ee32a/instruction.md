You are tasked with writing a Python configuration backup tool that processes system configuration files into a custom archive format while safely handling filesystem anomalies.

A previous version of our backup script crashed because a rogue configuration directory contained symlink loops, causing infinite recursion. We need a robust Python script to handle this.

Write a Python script at `/home/user/backup_manager.py` that fulfills the following requirements:

1. **Directory Traversal & Symlink Handling:**
   Walk through the directory `/home/user/config_root`. You must process all regular files, including those pointed to by symlinks, but you *must detect and prevent infinite recursion* caused by symlink loops. 
   Process the files in alphabetical order based on their resolved relative paths (relative to `/home/user/config_root/`).

2. **Memory-Mapped I/O:**
   For each uniquely discovered file, you must read its contents using Python's `mmap` module (assume files are small enough for mmap, but we enforce this for performance tracking).

3. **Custom Compression (RLE):**
   Compress the contents of each file using a custom Run-Length Encoding (RLE) scheme and write it as text. 
   - Encoding rule: For every sequence of identical characters, output the count followed by the character itself.
   - The maximum count per block is 9. If a character appears 12 times consecutively, it should be encoded as `9[char]3[char]`.
   - Example: `server=appp\n` becomes `1s1e1r1v1e1r1=1a3p1\n`.

4. **Archive Format:**
   The output should be a single text file. For each processed file, write a header line exactly like this:
   `---FILE: <relative_path>---`
   followed immediately by the RLE compressed data on the next line, followed by a newline.
   `<relative_path>` must be the relative path of the file from `/home/user/config_root/`.

5. **Atomic Writes:**
   The final archive must be saved to `/home/user/backup.ccf`. To prevent corruption if the script crashes, you *must* write the archive to a temporary file first, and then atomically rename/move it to `/home/user/backup.ccf`.

6. **Manifest Generation:**
   After writing the archive, generate a manifest file at `/home/user/manifest.log`. This file must list each processed file's relative path and its original uncompressed size in bytes, one per line, formatted as:
   `<relative_path>: <size_in_bytes>`

Run your script to produce `/home/user/backup.ccf` and `/home/user/manifest.log`.