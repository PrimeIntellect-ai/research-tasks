You are a storage administrator managing disk space on a Linux server. A legacy backup system recently went haywire due to following symlinks into infinite loops. The backup daemon was killed, but it left behind an audit log of the files it attempted to process.

Your task is to analyze this log and generate a cryptographic manifest of the files that were successfully backed up before the crash. 

Write a Python script at `/home/user/process_audit.py` that performs the following:

1. Reads the log file located at `/home/user/storage_audit.log`. The backup system is old and writes its logs in `UTF-16LE` encoding.
2. Parses the multi-line log records. Each record has the following format:
   ```
   === RECORD ===
   Path: <absolute_file_path>
   Type: <File|Symlink|Directory>
   Action: <BackedUp|InfiniteLoopAborted|Skipped>
   === END ===
   ```
3. Identifies all records where the `Action` is exactly `BackedUp`.
4. Computes the SHA-256 checksum for each successfully backed-up file (the files still exist on disk).
5. Writes a manifest file to `/home/user/backed_up_manifest.txt` containing the checksums and file paths.

The output manifest at `/home/user/backed_up_manifest.txt` must:
- Be encoded in standard UTF-8.
- Have exactly one line per successfully backed-up file.
- Be formatted as: `<sha256_hex> *<absolute_path>` (note the asterisk before the path, mimicking standard `sha256sum` output).
- Be sorted alphabetically by the absolute file path.

You may run your script to generate the output file. The automated verification will solely check the contents of `/home/user/backed_up_manifest.txt`.