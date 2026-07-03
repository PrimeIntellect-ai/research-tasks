I am a researcher organizing a large, messy dataset directory located at `/home/user/dataset`. Some automated tools have created recursive symlinks in this directory, forming infinite loops. 

I need you to write and execute a Python script (`/home/user/archive_dataset.py`) that searches for specific files, computes their checksums, and packs them into a custom binary archive format, all while avoiding the infinite symlink loops.

Here are the specific requirements:

1. **File Search:**
   - Search within `/home/user/dataset` for all files ending in `.dat` that are **strictly greater than 50 KB** (51,200 bytes) in size.
   - Ignore any symlinks to avoid infinite loops. Only process regular files.

2. **Manifest and Checksum Generation:**
   - For every valid file found, calculate its SHA-256 checksum. To do this efficiently, use streaming (reading in chunks) or memory-mapped I/O (`mmap`).
   - Create a manifest file at `/home/user/manifest.json`. It should be a JSON object where the keys are the relative paths of the files from the `/home/user/dataset` directory (e.g., `folder/file.dat`) and the values are their lowercase hex SHA-256 checksums.

3. **Custom Archive Format:**
   - Pack the valid files into a single custom binary archive located at `/home/user/archive.bin`.
   - The archive must contain the files sequentially. For each file, write the following exact sequence of bytes:
     1. **Path Length:** 2 bytes, little-endian unsigned integer representing the byte-length of the relative path string.
     2. **Relative Path:** The relative path string encoded in UTF-8 (e.g., `folder/file.dat`).
     3. **Original File Size:** 8 bytes, little-endian unsigned integer representing the uncompressed size of the file in bytes.
     4. **Compressed Data:** The file's data compressed using standard `zlib` compression (level 6).

Ensure your script runs successfully and creates both `/home/user/manifest.json` and `/home/user/archive.bin` with the exact specifications described.