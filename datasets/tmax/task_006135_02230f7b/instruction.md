You are an AI assistant helping a storage administrator consolidate and clean up disk space. We receive daily telemetry logs that are currently stored in deeply nested archives, taking up too much space with redundant debug data.

Your task is to write and execute a Python script that processes these nested archives, transforms the data, and creates a consolidated, space-efficient, multi-part backup.

Here are the requirements:

1. **Input Location**: The raw data is located in `/home/user/incoming_data`. This directory contains various archives (`.tar.gz`, `.tar`). Some of these archives may contain nested archives (e.g., `.zip` files inside a `.tar` file), alongside raw `.csv` files.

2. **Extraction and Merging**:
   - Recursively search through `/home/user/incoming_data` and process all `.csv` files, whether they are loose in the directory, inside a `.tar` / `.tar.gz`, or inside a `.zip` that is itself inside a tarball.
   - All `.csv` files share the exact same header: `timestamp,server_id,metric_value,status`.
   - Merge the contents of all discovered `.csv` files.

3. **Data Transformation (Filtering & Sorting)**:
   - Remove any rows where the `status` column is exactly `DEBUG`.
   - Remove any rows where the `metric_value` is less than `0`.
   - Sort all the remaining data rows in ascending order based on the `timestamp` column.

4. **Chunking and Compressed Output**:
   - Split the filtered, sorted data into chunks of exactly **500 data rows** per chunk (the final chunk may have fewer).
   - Every chunk must include the header row `timestamp,server_id,metric_value,status` at the top.
   - Compress each chunk using `gzip` and write them to `/home/user/clean_backups/`.
   - Name the files sequentially: `backup_part_001.csv.gz`, `backup_part_002.csv.gz`, etc.

5. **Manifest Generation**:
   - Create a JSON file at `/home/user/clean_backups/manifest.json`.
   - The JSON should be an object with a key `"processed_files"` mapping to a sorted list of the original `.csv` filenames (basenames only, no paths) that were successfully found and merged.
   
Please write and run the necessary Python code to achieve this. Let me know when the process is complete and the files are ready in `/home/user/clean_backups/`.