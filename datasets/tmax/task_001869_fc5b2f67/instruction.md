You are managing an artifact repository. Recently, a buggy incremental backup script followed a recursive symlink, creating a deeply nested "Russian doll" archive before eventually crashing. 

We have recovered the root archive at `/home/user/corrupted_backup.tar`. 

This archive contains a file named `layer_1.tar`. 
Inside `layer_1.tar` is a file named `layer_2.tar`, and so on. 
Deep within this structure, inside `layer_42.tar`, there is a binary artifact named `secret_artifact.bin` alongside the next layer archive.

Your task is to:
1. Write a Python script to traverse this deeply nested archive structure to access `secret_artifact.bin`.
2. Because of strict disk space and inode limits on this server, **you must not extract the archives to disk**. You must use Python's `tarfile` module to stream and process the nested archives in memory (e.g., using streaming I/O).
3. Once you access `secret_artifact.bin` (which is located inside `layer_42.tar`), compute its SHA256 checksum.
4. Write the resulting hex digest of the SHA256 checksum to `/home/user/artifact_hash.txt`.

Ensure your solution strictly uses Python and streaming I/O to avoid exhausting disk space.