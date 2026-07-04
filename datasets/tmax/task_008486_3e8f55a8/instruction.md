You are tasked with building a secure configuration archiving and synchronization system in C++. The system consists of a utility that can pack a directory into a custom archive format, and a daemon that watches a directory for new archives and extracts them safely.

We have a custom archive format called `.cfgpack`. It merges multiple configuration files into a single file with a manifest to ensure integrity. However, we need to ensure the extraction mechanism is resilient against path traversal attacks (often called "Zip Slip").

Your objective is to complete the C++ program `/home/user/pack_manager.cpp`.

### Phase 1: Dependencies and Skeleton
1. Ensure any necessary development dependencies for SHA-256 hashing (e.g., OpenSSL) and compilation are installed.
2. Create `/home/user/pack_manager.cpp`. You must implement two primary modes:
   * **Mode 1: Pack** (`./pack_manager pack <input_dir> <output_file>`)
   * **Mode 2: Watch** (`./pack_manager watch <watch_dir> <extract_dir>`)

### Phase 2: Packing (`pack` mode)
When running `./pack_manager pack <input_dir> <output_file>`:
1. Recursively traverse `<input_dir>`.
2. Generate a `.cfgpack` file that contains all regular files found.
3. **Format Specification for `.cfgpack`:**
   * The file must start with exactly `MANIFEST_START\n`.
   * For each file, write a line: `<relative_path>|<file_size_in_bytes>|<sha256_hex_string>\n`
     *(The `<relative_path>` should not start with `./` or `/`, e.g., `subdir/config.json`)*
   * Followed by `MANIFEST_END\n`.
   * Followed by `DATA_START\n`.
   * Followed immediately by the raw binary contents of all files concatenated in the exact order they appeared in the manifest.
   * Followed by `DATA_END\n`.

### Phase 3: Watching and Extracting (`watch` mode)
When running `./pack_manager watch <watch_dir> <extract_dir>`:
1. The program must use Linux `inotify` to monitor `<watch_dir>` for the `IN_CLOSE_WRITE` event on any file ending in `.cfgpack`.
2. Upon detection, it must read the archive, parse the manifest, and extract the chunks into `<extract_dir>`.
3. **Security (Zip Slip Prevention):** If any `<relative_path>` in the manifest is absolute (starts with `/`) or contains path traversal sequences (e.g., `../`, `..`, or ends with `/..`), the **entire** archive must be rejected. Do not extract any files from a malicious archive.
4. **Integrity:** Verify the SHA-256 hash of the extracted chunks. If a hash mismatch occurs, reject the file and delete the partially extracted file.
5. Create parent directories inside `<extract_dir>` as needed during extraction.

### Phase 4: Logging
Whenever a `.cfgpack` is processed by the watcher, append a multi-line log record to `/home/user/manager.log` in exactly this format:
```
[ARCHIVE EVENT]
File: <name_of_the_cfgpack_file>
Status: <SUCCESS | ERROR_PATH_TRAVERSAL | ERROR_INTEGRITY>
Files Processed: <number_of_files_successfully_extracted_or_0_if_error>
```

### Final Steps
Compile your program to `/home/user/pack_manager`.
Run it in the background:
`./pack_manager watch /home/user/dropzone /home/user/configs &`

Ensure `/home/user/dropzone` and `/home/user/configs` exist before running the daemon.