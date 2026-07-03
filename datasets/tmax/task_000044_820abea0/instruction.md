You are helping a developer organize a messy directory of project assets located at `/home/user/project_assets`. The files in this directory have lost their extensions, and some files have been corrupted.

Your task is to write and execute a Python script to process these files and generate a summary report. You must perform the following steps:

1. Scan all files in the `/home/user/project_assets` directory.
2. Identify which files are ZIP archives by reading their first 4 bytes (the ZIP magic number is `50 4B 03 04` in hex).
3. For the files identified as ZIP archives, verify their archive integrity. Ignore any corrupted archives.
4. For the valid ZIP archives, search inside them for a file exactly named `metadata.json`.
5. Extract the JSON data from `metadata.json` (which contains `asset_id`, `type`, and `version` keys).
6. Consolidate this data and convert it into a single CSV file located at `/home/user/asset_report.csv`.

The final CSV file must have the following exact characteristics:
- The first row must be the header: `filename,asset_id,type,version`
- Subsequent rows must contain the data from the valid ZIP files that contained `metadata.json`.
- The `filename` column should be the name of the file in the `/home/user/project_assets` directory (e.g., `file_A`).
- The rows must be sorted alphabetically by the `filename` column.

If a file is not a ZIP archive, is corrupted, or does not contain `metadata.json`, it should be excluded from the final report.