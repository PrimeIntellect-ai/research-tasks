You are tasked with fixing a backup pipeline for a developer's project files. A recent misconfiguration caused a backup script to follow symlinks into infinite loops, crashing the backup server. 

You must write a C++ sanitisation program that filters out dangerous paths from a backup manifest, and then glue together the indexing and storage services to use your filter.

### 1. The C++ Filter Program
Write a C++ program at `/home/user/filter_manifest.cpp` and compile it to `/home/user/filter_manifest`.
Your program must accept three arguments:
`./filter_manifest <base_dir> <input_manifest> <output_manifest>`

**Manifest Format (Binary):**
- **Header:** Exactly 8 bytes: `BKP_MNFS`
- **Entries:** Follow immediately until EOF.
  - Path Length (`L`): 2-byte unsigned integer (little-endian).
  - Path: `L` bytes representing the relative file path (UTF-8).
  - Checksum: 32 bytes of raw SHA-256 binary data.

**Filtering Logic:**
Your program must read the input manifest (using streaming I/O or memory mapping) and write a new manifest to the output.
For each entry, you must prepend `<base_dir>` to the relative path and resolve it. 
An entry is **safe** (and should be copied to the output manifest) IF AND ONLY IF:
1. The path resolves successfully without infinite symlink loops.
2. The completely resolved absolute path strictly resides within the absolute path of `<base_dir>`.

Any entry that causes a symlink loop, does not exist, or points outside `<base_dir>` must be silently dropped. The output manifest must retain the 8-byte header and exactly the safe entries. 

*Hint: Standard library functions like `realpath` or `std::filesystem::canonical` can help detect loops and directory escapes.*

### 2. Multi-Service Pipeline
There are two services running on the local machine:
- **`file_indexer`**: Listens on TCP port 9001. When connected, it streams the raw, unfiltered binary manifest and closes the connection.
- **`backup_storage`**: Listens on TCP port 9002. It expects to receive a filtered binary manifest and will store the backup.

Write a bash script at `/home/user/run_pipeline.sh` that connects these services using your C++ program. The script should pull the manifest from port 9001, pipe it through your filter (you can use `/dev/stdin` and `/dev/stdout` for the manifest arguments), with `/home/user/project_root` as the `<base_dir>`, and send the filtered output directly to port 9002.

Make sure to compile your C++ code and ensure your bash script is executable.