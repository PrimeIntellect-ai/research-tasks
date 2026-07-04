You are a storage administrator managing a custom backup system. A set of backups has been chunked and distributed, but we need to restore them. However, we suspect the backup manifest might have been tampered with to include path traversal attacks (similar to a zip-slip vulnerability) that attempt to overwrite system files outside the designated restore directory.

Your task is to write and execute a Rust program that safely reconstructs the files from the chunks based on a JSONL manifest.

Environment:
- Workspace: `/home/user/storage_task/`
- Manifest file: `/home/user/storage_task/manifest.jsonl`
- Chunks directory: `/home/user/storage_task/chunks/`
- Target restore directory: `/home/user/storage_task/restored/` (You must create this directory)
- Rejected log file: `/home/user/storage_task/rejected.log`

Manifest Format (`manifest.jsonl`):
Each line is a JSON object with the following fields:
- `chunk`: String. The name of the chunk file in the `chunks/` directory (e.g., "chunk_0.bin").
- `target`: String. The intended relative path for the restored file (e.g., "reports/summary.txt").
- `offset`: Integer. The byte offset where this chunk should be written in the target file.

Requirements for your Rust program:
1. Parse the `manifest.jsonl` file.
2. For each entry, resolve the `target` path against the target restore directory (`/home/user/storage_task/restored/`).
3. **Security Check**: You must rigorously verify that the resolved target path is strictly inside the `/home/user/storage_task/restored/` directory. Be aware of absolute paths or directory traversal payloads (e.g., `../`). 
4. If a target path attempts to escape the restore directory, do NOT write the chunk. Instead, append the exact `target` string from the JSON to `/home/user/storage_task/rejected.log` (one per line).
5. If the target path is safe, ensure the parent directories for the target file exist, open the target file, seek to the specified `offset`, and write the entire contents of the chunk file. You must use streaming I/O or `seek` to place the chunks correctly, as chunks for the same file may arrive out of order.
6. Create a Cargo project in `/home/user/storage_task/restorer/` and write your solution there. You may use standard crates like `serde` and `serde_json`.
7. Compile and run your program to perform the restoration.

Ensure the final restored files have the exact binary contents as constructed by the safe chunks, and `rejected.log` contains all malicious paths.