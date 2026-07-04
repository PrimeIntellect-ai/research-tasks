I need you to act as an artifact manager and curate a repository of binary files. I have an archive located at `/home/user/raw_artifacts.tar.gz`. 

Please perform the following steps:
1. Extract the archive into a new directory: `/home/user/workspace/`.
2. Inside the workspace, you will find a `bin/` directory containing various binary files and a multi-line log file named `artifact_registry.log`.
3. The `artifact_registry.log` file contains records of these binaries. Each record is exactly 5 lines long, separated by a newline if there are subsequent records. The format is:
```
[Record Start]
Artifact ID: <integer>
File: <relative path to binary>
Expected Magic: <4-byte hex string, e.g., 0xDEADBEEF>
Status: UNVERIFIED
```
4. For each record in the log, read the corresponding binary file from the workspace. Extract the first 4 bytes of the binary file and interpret them as a big-endian hexadecimal integer.
5. Compare the extracted 4-byte magic number with the `Expected Magic` value in the log.
6. If the magic number matches:
   - Keep the file.
   - Update the `Status:` line in that log record from `UNVERIFIED` to `VERIFIED`.
7. If the magic number does NOT match (or the file is missing/unreadable):
   - Delete the corrupted binary file from the disk.
   - Remove the entire 5-line record for this artifact from `artifact_registry.log`. Make sure not to leave extra blank lines where the record used to be (the remaining records should still be back-to-back, exactly 5 lines each).
8. Once all files and log records have been processed, create a new compressed archive at `/home/user/curated_artifacts.tar.gz`. This archive must contain the updated `artifact_registry.log` and the `bin/` directory with the remaining valid binaries. The root of the archive should be the contents of the `workspace` directory (i.e., when extracting the new archive, `artifact_registry.log` and `bin/` should be in the current directory, not wrapped in an outer `workspace` folder).

Use Python to write a script to automate this curation process.