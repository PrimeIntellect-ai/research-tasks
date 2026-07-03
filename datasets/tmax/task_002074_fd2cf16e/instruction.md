You are acting as a configuration manager for a newly deployed environment. The system has dumped a set of raw configuration files into an archive, but they contain sensitive debugging tokens, have arbitrary names, and need to be strictly version-controlled.

Your task is to sanitize, rename, and package these configurations using a combination of a Go script and standard shell commands.

Here are the specific steps you must complete:

1. **Extract Initial Archive:**
   Extract the archive located at `/home/user/raw_configs/configs.tar.gz` into the directory `/home/user/configs/`.

2. **Process Configurations (via Go):**
   Write a Go program at `/home/user/process_configs.go` and run it. This program must:
   - Read every `.json` file in `/home/user/configs/`.
   - Parse the JSON content. Each file contains at least a `"service"` (string) and `"version"` (string) key.
   - If a key named `"debug_token"` exists in the JSON, remove it.
   - Serialize the sanitized JSON data.
   - Perform an **atomic write** of the new JSON to a new directory `/home/user/processed_configs/`. To do this, your Go code must write the sanitized JSON to a temporary file in `/home/user/processed_configs/`, and then atomically rename it to the final filename.
   - The final filename must follow the pattern: `<service>_v<version>.json` (e.g., if service is "web" and version is "2.0", the file should be `web_v2.0.json`).

3. **Generate a Manifest:**
   Using shell tools, generate a SHA256 checksum manifest of all the sanitized JSON files inside `/home/user/processed_configs/`.
   Save this manifest to `/home/user/manifest.txt`. The manifest should be generated exactly as the output of running `sha256sum *` from inside the `processed_configs` directory.

4. **Package the Results:**
   Create a new tar gzip archive at `/home/user/final_configs.tar.gz`. This archive must contain:
   - The `processed_configs` directory (and all its `.json` contents).
   - The `manifest.txt` file.

Make sure your Go code handles errors appropriately and executes successfully.