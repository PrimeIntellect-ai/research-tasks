You are acting as a systems engineer developing a secure configuration manager. Our servers send backup configuration archives, but we suspect a compromised server is sending malicious archives attempting a "tar slip" (or zip slip) attack to overwrite files outside the target extraction directory using path traversal (`../`) and malicious symbolic links.

Your task has three main phases:

**Phase 1: Chunk Merging and Integrity Verification**
In `/home/user/incoming/`, you will find a directory called `chunks/` containing several file chunks (`backup.tar.gz.part-00`, `backup.tar.gz.part-01`, etc.) and a checksum file `checksums.sha256`. 
1. Verify the integrity of all chunks using the provided SHA256 checksum file.
2. Merge the chunks in the correct order to reconstruct the original archive at `/home/user/workspace/merged.tar.gz`.

**Phase 2: Secure Extractor Development (Rust)**
You must write a Rust program to safely extract this archive. Create a new Cargo project at `/home/user/workspace/secure_extractor`.
Write a program that takes two arguments: the path to the tar.gz archive, and the destination directory.
The program must:
1. Use the `tar` and `flate2` crates to read the gzipped tarball.
2. Iterate through the entries and extract them to the destination directory.
3. **Security Rule 1:** If an entry's path contains `..` components or is an absolute path (starts with `/`), it must NOT be extracted.
4. **Security Rule 2:** If an entry is a symbolic link or hard link, you must verify that its target does not point outside the destination directory. If it does (or if it's absolute), it must NOT be extracted.
5. Whenever an entry is skipped due to these security rules, append a line to `/home/user/workspace/extraction.log` in the exact format: `SKIPPED: <path_as_stored_in_archive>`.

**Phase 3: Execution**
1. Build your Rust project.
2. Create the destination directory `/home/user/workspace/safe_configs/`.
3. Run your compiled Rust program on `/home/user/workspace/merged.tar.gz`, extracting it to `/home/user/workspace/safe_configs/`.

When you are finished, the valid configurations should be located in `/home/user/workspace/safe_configs/`, and the malicious attempts should be logged in `/home/user/workspace/extraction.log`.