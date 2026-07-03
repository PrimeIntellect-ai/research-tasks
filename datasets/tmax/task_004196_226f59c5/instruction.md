You are acting as a configuration and deployment tracking agent for a hybrid edge node that handles software binaries, 3D printing tasks, and local database transactions.

Your task is to write and execute a Bash script at `/home/user/config_tracker.sh` that analyzes deployment logs, inspects the deployed files, extracts domain-specific metadata, and generates tracking manifests.

Here are the requirements for your script:

1. **Parse the Deployment Log:**
   Read the multi-line log file located at `/home/user/deploy.log`. This log contains blocks of text describing deployment events. Each block begins with `=== DEPLOYMENT ===`.
   You must identify the `File:` path for deployments where the `Status:` is exactly `SUCCESS`. Ignore `FAILED` deployments.

2. **Extract Metadata based on File Type:**
   For each successfully deployed file, determine its type and extract specific metadata:
   *   **ELF Binary:** If the file is an ELF executable (you can verify this using the `file` command or by extension if you prefer, but the actual files have a `.bin` extension), use `readelf -h` to extract the "Entry point address". Format it exactly as output by `readelf` (e.g., `0x401000` or `0x401040`).
   *   **GCode:** If the file ends with `.gcode`, parse the file to find the comment line starting with `; estimated printing time =`. Extract the time given in the format `Xh Ym Zs` and convert it to total minutes (rounded down to the nearest minute). For example, `1h 25m 10s` becomes `85`.
   *   **SQLite WAL:** If the file ends with `.wal` (Write-Ahead Log), extract its magic number. Read the first 4 bytes of the file and format them as a continuous lowercase hexadecimal string (e.g., `377f0682`). You can use `xxd`, `od`, or `hexdump`.

3. **Format Conversion (CSV):**
   Output the extracted information to a CSV file at `/home/user/deploy_metadata.csv`.
   The CSV must have the following header: `FilePath,FileType,Metadata`
   *   `FileType` must be one of `ELF`, `GCODE`, or `WAL`.
   *   `Metadata` is the extracted value (Entry point address, total minutes, or magic number).
   *   Sort the rows alphabetically by `FilePath`.

4. **Manifest and Checksum Generation:**
   Generate a SHA256 checksum for each of the successfully deployed files.
   Write the results to `/home/user/deploy_manifest.sha256` in the standard format output by `sha256sum`.
   Sort the output alphabetically by the file path.

Once you have written the script, execute it so that `/home/user/deploy_metadata.csv` and `/home/user/deploy_manifest.sha256` are created and populated. Do not change the permissions or state of the deployed files.