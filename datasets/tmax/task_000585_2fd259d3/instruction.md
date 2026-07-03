You are tasked with building a gRPC-based directory synchronization tool in Python to help developers organize and synchronize project files between different versions. 

You need to build a system that analyzes two directories, computes the differences using a custom data structure, and provides gRPC endpoints to retrieve the differences and apply them.

Please implement the following in the directory `/home/user/dir_sync`:

1. **Protocol Buffer Definition (`/home/user/dir_sync/sync.proto`)**
   Define a gRPC service named `DirSync` in package `sync`.
   It must have the following RPC methods:
   - `CalculateDiff(DiffRequest) returns (DiffResponse)`
   - `ApplyPatch(PatchRequest) returns (PatchResponse)`

   Messages:
   - `DiffRequest`: Contains two string fields `source_dir` and `target_dir` (absolute paths).
   - `DiffResponse`: Contains a repeated string field `patch_lines` (representing the combined unified diff of all modified/added/deleted files).
   - `PatchRequest`: Contains a string field `target_dir` (absolute path) and a repeated string field `patch_lines`.
   - `PatchResponse`: Contains a boolean field `success`.

2. **gRPC Server (`/home/user/dir_sync/server.py`)**
   Implement the server listening on `localhost:50051`.
   - `CalculateDiff`: Must build a custom tree data structure (e.g., a custom prefix tree or Merkle tree of the directory structure) to efficiently identify files that differ between `source_dir` and `target_dir`. For differing text files, it should generate a unified diff (using Python's `difflib` or the `diff -u` system command). The result is returned as a list of patch lines in `patch_lines`. Note that the unified diff should use relative paths to the root of the directories.
   - `ApplyPatch`: Takes the `patch_lines` and applies them to the `target_dir` (using the system's `patch` utility or custom logic). Returns `success = True` if the patch applied cleanly.

3. **End-to-End Orchestration (`/home/user/dir_sync/run_e2e.sh`)**
   Write a bash script that:
   - Compiles the protobuf file using `grpc_tools.protoc`.
   - Creates two directories: `/home/user/dir_sync/test_a` and `/home/user/dir_sync/test_b`.
   - Populates them with some differing text files.
   - Starts the `server.py` in the background.
   - Uses a client (you should write `/home/user/dir_sync/client.py` for this) to call `CalculateDiff` comparing `test_a` and `test_b`, then calls `ApplyPatch` to apply the diff to `test_a` so it matches `test_b`.
   - Verifies the directories are now identical using `diff -r`. If successful, the script should print `E2E TEST PASSED` to standard output.
   - Kills the background server.

Requirements:
- Ensure all file paths in the generated patches are relative to the directory roots.
- Use Python 3. You may install standard gRPC dependencies (`grpcio`, `grpcio-tools`).
- The custom data structure must explicitly recursively hash or compare file sizes/mtimes/contents to prune unchanged subtrees.

Your final goal is a fully working `run_e2e.sh` that exits with code 0 and outputs `E2E TEST PASSED`.