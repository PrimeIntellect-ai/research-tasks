You are a storage administrator tasked with reclaiming disk space and standardizing an archive of legacy system logs. 

You have a directory at `/home/user/raw_logs` containing daily log exports. These files have verbose names, are encoded in an older `iso-8859-1` format, and contain large amounts of useless "SUCCESS" events and comment lines.

To optimize storage, you need to write and execute a Python script that processes these files and saves the minimized, standardized versions to `/home/user/processed_logs`. Because new logs arrive daily and space is at a premium, your script must act like an incremental backup: it should only process files that haven't been processed before.

Here are the exact requirements:

1. **Bulk Renaming Logic**: Original files are named in the format `System Log - YYYY-MM-DD - <NodeID>.csv`. Your script must determine the output filename as `log_<YYYYMMDD>_<NodeID>.csv`. For example, `System Log - 2023-10-02 - N01.csv` becomes `log_20231002_N01.csv`.
2. **Incremental Processing**: Read the file `/home/user/processed_manifest.txt`. This file contains a list of already processed target filenames (one per line). If a calculated target filename is already in the manifest, **skip** processing that original file entirely.
3. **Character Encoding Conversion**: Read the original files using `iso-8859-1` encoding and write the processed files using `utf-8` encoding.
4. **Large-Scale Text Editing / Filtering**: When processing a file:
   - Completely remove any line that starts with the `#` character (ignoring leading whitespace).
   - Completely remove any data row where the `status` column (the 3rd column, comma-separated) equals exactly `SUCCESS`.
   - Keep the header row (which does not start with `#` and has `status` as the column name) and all lines where the status is `FAILED` or `ERROR`.
5. **Output**: Save the filtered, UTF-8 encoded files into `/home/user/processed_logs/` using the new filename.
6. **Manifest Update**: Append the new target filename to `/home/user/processed_manifest.txt` immediately after processing it, so it won't be processed again in future runs.

**Starting State:**
- Input directory: `/home/user/raw_logs`
- Output directory: `/home/user/processed_logs` (you must create this directory if it doesn't exist)
- Manifest file: `/home/user/processed_manifest.txt`

Write the Python script, execute it, and ensure the processed logs and the updated manifest match the specifications.