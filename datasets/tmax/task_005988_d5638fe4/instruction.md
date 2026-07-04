You are a storage administrator managing disk space on a critical server. You need to identify redundant and error-filled files that can be archived or deleted. 

A backup directory is located at `/home/user/storage_dumps` and contains a nested hierarchy of text logs (`.log`) and binary data dumps (`.dat`). 

Your task is to write a Python script at `/home/user/find_waste.py` that performs the following:
1. Recursively traverses the `/home/user/storage_dumps` directory.
2. Identifies specific `.log` files: A `.log` file should be flagged if it contains a multi-line error record that starts with `[CRITICAL]` on one line and ends with `[END CRITICAL]` on a subsequent line (with any content in between).
3. Identifies specific `.dat` files: A `.dat` file should be flagged if it contains the exact byte sequence `\xde\xad\xbe\xef` at exactly byte offset 1024. You must use memory-mapped I/O (`mmap`) to read the `.dat` files. Files smaller than 1028 bytes can be safely ignored.
4. Calculates the total size (in bytes) of all flagged files (both `.log` and `.dat`).
5. Writes the final total size to `/home/user/reclaimable_space.txt` in the exact format: `Total bytes: <number>`. 
6. The write operation to `/home/user/reclaimable_space.txt` MUST be atomic (i.e., write the output to a temporary file first, then atomically rename it to the final destination path).

Once your script is written, run it so that `/home/user/reclaimable_space.txt` is generated.