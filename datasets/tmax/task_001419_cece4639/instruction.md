You are assisting a security-conscious researcher in organizing a massive dataset of multi-line sensor logs collected from various edge devices. 

The edge devices upload data in a proprietary, uncompressed archive format. We only have a legacy, stripped binary tool located at `/app/extractor` that can unpack these archives. You can test how it works by running it.

**The Problem:**
The `/app/extractor` binary is known to be vulnerable to a "Zip Slip" style path traversal attack. If an archive contains entries with absolute paths (e.g., `/etc/passwd`) or parent directory references (e.g., `../root_key`), the extractor will blindly write files to those locations, potentially overwriting critical system files. 

**Your Objectives:**

1. **Write a C-based Archive Sanitizer:**
   Write a C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`. 
   This program must act as a filter. It should take exactly one argument (the path to an archive file) and parse the custom archive format just enough to read the file paths embedded within it.
   - If **any** file path in the archive is absolute (starts with `/`) or contains path traversal sequences (`../`), the program must terminate with exit code `1` (Reject).
   - If **all** file paths in the archive are safe, the program must terminate with exit code `0` (Accept).
   - *Note:* You will need to reverse-engineer the basic header structure of the archives by examining the files in the provided datasets or interacting with `/app/extractor`.

2. **Verify Against Corpora:**
   The researcher has provided two directories of archives:
   - `/home/user/dataset/clean/`: Contains 50 safe archives.
   - `/home/user/dataset/evil/`: Contains 50 malicious archives with path traversal payloads.
   Your `sanitizer` must successfully exit `0` for all files in the `clean` directory, and exit `1` for all files in the `evil` directory.

3. **Safe Extraction, Bulk Renaming, and Manifest Generation:**
   Once your sanitizer is working, use it to identify the safe archives in `/home/user/dataset/clean/`. 
   For each safe archive:
   - Extract its contents into `/home/user/dataset/extracted/`.
   - The extracted files will be multi-line `.log` files. Calculate the SHA-256 checksum of each extracted file.
   - Rename every extracted file to its checksum: `<sha256_hash>.log`.
   - Generate a manifest file at `/home/user/dataset/manifest.txt` where each line is formatted exactly as: `<sha256_hash> <original_filename_from_archive>` (separated by a single space).

Ensure your C code is robust and does not crash on malformed inputs.