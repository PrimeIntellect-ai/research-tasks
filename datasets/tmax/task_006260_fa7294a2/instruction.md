You are an artifact manager responsible for curating binary repositories. You have been provided with an exported snapshot of our local artifact registry, located at `/home/user/artifact_repo.tar.gz`.

Your task is to identify which artifacts have corrupted binaries based on their build logs. 

Follow these exact steps:
1. "Mount" the repository by extracting the contents of `/home/user/artifact_repo.tar.gz` into a new directory: `/home/user/repo_mount`.
2. Inside `/home/user/repo_mount`, you will find an `artifacts/` directory containing several subdirectories, each named after an artifact (e.g., `artifacts/libA/`, `artifacts/libB/`).
3. Inside each artifact's directory, there is a gzip-compressed log file named `build.log.gz`.
4. You need to parse these compressed log streams. The log files contain multi-line entries. Every log entry strictly begins with a timestamp in brackets, e.g., `[2023-10-24 12:00:00]`. If a line does not start with `[`, it is a continuation of the previous log entry.
5. Search for log entries that begin with `[YYYY-MM-DD HH:MM:SS] FATAL_ERROR:`. 
6. Read the entire multi-line block of that `FATAL_ERROR`. If the block contains a line with the exact text `Reason: Checksum mismatch` anywhere before the next log entry begins, that artifact is considered corrupted.
7. Collect the names of all corrupted artifacts (the artifact name is the name of its directory, e.g., `libB`).
8. Create a log file at `/home/user/corrupted_artifacts.txt` containing the names of the corrupted artifacts. Write one artifact name per line, sorted alphabetically.

Ensure you process the compressed files directly or securely within the mount directory, and accurately group the multi-line log records to avoid false positives from other error types.