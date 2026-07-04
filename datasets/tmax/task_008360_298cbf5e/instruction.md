You are an AI assistant helping a bioinformatics researcher organize incoming dataset packages. The datasets are delivered as tarball archives (`.tar.gz`) from various external laboratories.

Some external labs use flawed archiving tools that accidentally (or maliciously) include absolute paths or directory traversal payloads (like `../`) in their tarballs, which could overwrite files outside the extraction directory. We need a robust Bash script to safely process these datasets.

Your task is to write and execute a Bash script located at `/home/user/process_datasets.sh`. The script must process all `.tar.gz` files found in `/home/user/incoming/`.

For each archive, the script must perform the following exactly:
1. **Security Audit**: Inspect the contents of the archive (without extracting it first) to check for directory traversal vulnerabilities. If ANY file inside the archive contains `../` or begins with `/`, do NOT extract the archive. Write exactly `SKIPPED: <filename> - ILLEGAL PATHS` to the log file at `/home/user/processing.log`.
2. **Safe Extraction**: If the archive is safe, extract it to a temporary directory.
3. **Metadata Parsing**: Inside the extracted archive, there will be a file named `metadata.conf`. It contains key-value pairs separated by an equals sign (e.g., `Project=Genomics`). Read the `Project` and `LabCode` values.
4. **Data Redaction**: Find all `.tsv` files within the extracted archive. Using `sed` or `awk`, redact any patient identifiers. Replace any string matching the pattern `PAT-[0-9][0-9][0-9][0-9]` with `PAT-REDACTED`. Modifiy the files in place or save the results.
5. **Organization**: Create the target directory `/home/user/organized/<Project>/<LabCode>/`. Copy the redacted `.tsv` files into this directory.
6. **Logging**: After successfully processing an archive, write exactly `PROCESSED: <filename> - <Project> - <LabCode>` to `/home/user/processing.log`.

Execute your script to process the datasets.

**Initial State:**
- The incoming datasets are in `/home/user/incoming/`.
- Ensure your script handles files with spaces in their names if they exist.

Provide the final `process_datasets.sh` script and ensure `/home/user/processing.log` and the `/home/user/organized/` directory are generated perfectly.