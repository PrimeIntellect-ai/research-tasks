You are an operations engineer tasked with creating a robust Python backup script for a tricky file system structure. 

The directory `/home/user/source_data` needs to be backed up, but it contains legacy recursive symlinks that form infinite loops. Standard backup scripts crash or run out of memory when encountering these loops.

Your task is to write and execute a Python script at `/home/user/safe_backup.py` that performs the following operations:

1. **Loop-Resistant Traversal**: Traverse `/home/user/source_data`, identifying and skipping any symlinks that result in an infinite loop. You must resolve absolute paths to detect if a directory has already been visited in the current path chain. Valid symlinks that do not form loops should be followed.
2. **Nested Archiving**: For each top-level directory inside `/home/user/source_data`, create a corresponding `.tar.gz` archive of its valid contents. Place these nested archives inside a temporary staging directory `/home/user/staging/`.
3. **Manifest & Checksum Generation**: Calculate the SHA256 hash of every valid, physical regular file encountered (do not hash directories or the symlinks themselves, but do hash the target files of valid symlinks). 
4. **Atomic Write**: Write these checksums to a JSON manifest file in the staging directory (`/home/user/staging/manifest.json`). The format must be a dictionary mapping the file's path (relative to `/home/user/source_data`) to its SHA256 hex digest. To prevent corruption if the script is interrupted, you **must** use an atomic write pattern for this manifest (write to `manifest.json.tmp` first, then atomically rename it to `manifest.json`).
5. **Final Archive**: Once the staging directory contains the nested `.tar.gz` archives and the `manifest.json`, package the entire contents of `/home/user/staging/` into a single, uncompressed tarball at `/home/user/final_backup.tar`.

After writing the script, execute it so that `/home/user/final_backup.tar` is successfully generated.