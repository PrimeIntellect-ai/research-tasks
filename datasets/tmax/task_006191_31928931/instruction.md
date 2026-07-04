You are acting as a storage administrator tasked with managing and consolidating disk space. We have received an old nested archive containing historical log data that needs to be flattened, verified, and safely stored in a new location.

Your task is to write a Rust program (you can create a Cargo project at `/home/user/consolidator`) that performs the following steps:

1. **Read and Extract**: Read a nested archive located at `/home/user/incoming/nested_logs.tar.gz`. This archive contains other `.tar.gz` files. You must extract the outer archive and all inner archives to discover all the underlying `.log` files.
2. **Checksum Generation**: For every `.log` file found in the inner archives, compute its SHA-256 checksum.
3. **Consolidation**: Create a new, flat, un-nested archive named `consolidated.tar.gz` that contains all the discovered `.log` files at its root level (do not include the intermediate directory paths in the new tarball).
4. **Manifest Creation**: Create a file named `manifest.json` containing a JSON object mapping the base filename of each `.log` file to its hex-encoded SHA-256 checksum. Format: `{"file1.log": "hash1", "file2.log": "hash2"}`.
5. **Atomic Writes**: To prevent partial data corruption in case of failure, your Rust program MUST write `consolidated.tar.gz` and `manifest.json` atomically to `/home/user/archive_dest/`. Specifically, write them to temporary files in `/home/user/archive_dest/` (e.g., ending in `.tmp`) and then use atomic rename operations to rename them to their final filenames.

**Constraints & Details:**
- The destination directory `/home/user/archive_dest/` already exists.
- You must use Rust to implement the logic. You may use standard crates like `tar`, `flate2`, `sha2`, `serde`, and `serde_json`. 
- Leave the compiled binary or Cargo project intact so we can review the code, but you must run the program so that the final files exist in `/home/user/archive_dest/`.