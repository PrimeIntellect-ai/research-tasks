You are a storage administrator managing disk space and security for a backup system. We have discovered that some legacy backup archives contain malicious paths attempting a "Zip Slip" directory traversal attack, trying to overwrite files outside their designated extraction directory. 

We need you to write a Python script at `/home/user/parser.py` that processes the archive manifests, calculates the required disk space for safe files, and generates a safe extraction plan.

Here are the requirements:

1. **Configuration Parsing**: Read the configuration file located at `/home/user/config/backup_system.ini`. This INI file contains a `[manifests]` section where keys are absolute paths to manifest files and values are their respective text encodings.
2. **Data Parsing & Encoding Conversion**: Read each manifest file listed in the INI file using the specified encoding. Each line in a manifest contains a file path and its size in bytes, separated by a space (e.g., `some/path/file.txt 1024`).
3. **Zip Slip Prevention**: Evaluate each file path as if it were to be extracted into `/home/user/extract/`. Resolve the path and ensure it strictly resides within `/home/user/extract/`. For example, `../evil.sh` would resolve to `/home/user/evil.sh` which is outside the target directory and must be flagged as malicious.
4. **Atomic Output**: Aggregate the results and write them to `/home/user/safe_extraction_plan.json`. You must write the output to a temporary file first and then use an atomic rename (e.g., `os.replace`) to write the final destination.

The final `/home/user/safe_extraction_plan.json` must be UTF-8 encoded and match this exact structure:
```json
{
  "total_safe_bytes": <integer sum of sizes of all safe files>,
  "safe_files": [
    "<original path string of safe file 1>",
    "<original path string of safe file 2>"
  ],
  "malicious_files_skipped": <integer count of files that escaped the target dir>
}
```
*Note: The `safe_files` array must contain the original relative paths from the manifests, but properly decoded to UTF-8 strings. Sort the `safe_files` list alphabetically.*

Write the script and execute it to generate the JSON file.