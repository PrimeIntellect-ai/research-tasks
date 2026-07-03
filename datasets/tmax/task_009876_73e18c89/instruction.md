You are an AI assistant acting as an artifact manager curating a local binary repository. 

Your task is to write a Python script at `/home/user/curate_artifacts.py` that processes a large artifact curation log and validates the physical presence of the binaries while gracefully avoiding infinite symlink loops present in the repository.

**Repository Structure & Context:**
- The repository is located at `/home/user/artifact_repo/`.
- Inside this directory, there is a sub-directory `/home/user/artifact_repo/binaries/` which contains the actual binary files. 
- *Warning:* A previous flawed backup script created several recursive symlinks inside the `binaries/` directory (e.g., symlinks pointing to their own parent directories, creating infinite loops).
- The log file is located at `/home/user/artifact_repo/curation.log`.

**Log Format:**
The log file `curation.log` is a large text file containing concatenated multi-line JSON objects separated by a line containing exactly `---`. 
Example:
```json
{
  "artifact_id": "pkg-101",
  "path": "binaries/v1/core.bin",
  "checksum": "a1b2c3d4",
  "status": "staged"
}
---
{
  "artifact_id": "pkg-102",
  "path": "binaries/v2/latest/util.bin",
  "checksum": "e5f6g7h8",
  "status": "staged"
}
---
```

**Your Objective:**
Write a Python script `/home/user/curate_artifacts.py` that does the following:
1. **Streaming I/O:** Read `/home/user/artifact_repo/curation.log` in a memory-efficient, streaming manner. Do not load the entire file into memory at once. Parse the multi-line JSON records sequentially.
2. **Validation & Loop Avoidance:** For each parsed record where `"status": "staged"`, resolve its `"path"` (which is relative to `/home/user/artifact_repo/`). You must determine if the file actually exists on disk. You must safely handle or bypass infinite symlink loops without crashing the script.
3. **File Locking:** If the artifact file exists and is valid (not caught in a symlink loop), extract its `artifact_id`, `path`, and `checksum`. Append these details to `/home/user/artifact_repo/valid_inventory.csv`. Because other curation tools might be reading this CSV concurrently, your script MUST acquire an exclusive file lock (`fcntl.flock` or `fcntl.lockf`) on the CSV file before writing each batch or record, and release it afterward.
4. **Output Format:** The output CSV should have the following headers: `ArtifactID,ResolvedPath,Checksum`. The `ResolvedPath` should be the absolute, fully resolved path to the file.

Execute your script to generate `/home/user/artifact_repo/valid_inventory.csv`.