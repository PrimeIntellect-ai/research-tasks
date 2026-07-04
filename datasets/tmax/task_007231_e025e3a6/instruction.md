As a storage administrator, you are tasked with managing disk space and sanitizing a poorly constructed log archive sent by a client. The archive is located at `/home/user/incoming/logs.tar.gz`.

We suspect this archive was created with a flawed script that included dangerous relative path traversals (e.g., `../`) and deep directory structures. If extracted normally, it could overwrite critical files outside the target directory (a "zip slip" vulnerability) or create an unnecessarily deep folder hierarchy.

Your task is to safely process this archive using only standard Bash shell tools. Write a script at `/home/user/cleanup.sh` and execute it to perform the following steps:

1. **Safe Extraction (Flattening):** Safely extract the contents of `/home/user/incoming/logs.tar.gz` into the directory `/home/user/safe_zone`. To prevent path traversal and save inode space from empty directories, you **must completely flatten** the directory structure. All files within the archive must end up directly in `/home/user/safe_zone` without any subdirectories.

2. **Configuration Interpretation:** Read the configuration file at `/home/user/admin.conf`. It contains standard `KEY=value` pairs. Extract the values for `REDACT_PATTERN` (a basic regular expression for matching sensitive data) and `SPLIT_LINES` (an integer).

3. **Format Conversion & Redaction:** Iterate over all the files now safely located in `/home/user/safe_zone`:
   - If a file has a `.csv` extension, convert it to a `.tsv` (Tab-Separated Values) file by replacing all commas with tabs. Ensure the new file has a `.tsv` extension and remove the original `.csv` file.
   - For all files in the directory (including the newly created `.tsv` files), use the `REDACT_PATTERN` regex from the config to find and replace all matching sensitive data with the literal string `***`. Edit the files in place.

4. **Chunking:** After redaction, check the line count of each file. If a file has more lines than the `SPLIT_LINES` value from the config, split it into smaller files, each containing `SPLIT_LINES` lines. Use the original filename as a prefix and append a standard alphabetical suffix (e.g., `.partaa`, `.partab`). After splitting, delete the original oversized file.

5. **Compression:** Finally, compress the processed contents of `/home/user/safe_zone` into a new bzip2-compressed tarball located at `/home/user/clean_logs.tar.bz2`. The archive should contain the files directly, or inside a single `safe_zone` directory (either is fine, as long as the cleaned files are inside).

Ensure your script handles all steps automatically.