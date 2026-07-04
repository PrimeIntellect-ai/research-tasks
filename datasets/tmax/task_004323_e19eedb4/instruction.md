I need your help organizing a messy dataset archive left behind by a former researcher. The archive is located at `/home/user/dataset_archive` and contains a deeply nested directory structure with various data files (`.dat`, `.log`, and `.csv`). 

Here is what I need you to do:

1. **Extract Error Logs (Text Transformation & Piping):**
   Navigate through the entire `/home/user/dataset_archive` directory tree. Find all `.log` files. Extract any line that starts exactly with `ERROR: CORRUPT_RECORD ID=`. 
   Using tools like `awk` or `sed`, transform these lines so that they only contain the ID and the timestamp (which appears at the end of the line in brackets). 
   Write the output to `/home/user/corruption_report.txt` in the exact format: `[ID] - [TIMESTAMP]`, sorted numerically by ID.
   *(Example input line: `ERROR: CORRUPT_RECORD ID=492 MSG=Invalid_Header [2023-10-01T12:00:00Z]` -> Example output: `492 - 2023-10-01T12:00:00Z`)*

2. **Fix Missing Metadata (Binary File Reading & Python):**
   Some of the binary dataset files (`.dat` extension) are missing their corresponding `.meta` files. A `.meta` file should have the exact same base name and exist in the same directory (e.g., `data1.dat` should have `data1.meta`).
   Write and execute a Python script at `/home/user/generate_meta.py` that finds all `.dat` files missing a `.meta` file. For each one, read exactly the first 8 bytes of the binary `.dat` file. Create the missing `.meta` file and write the hexadecimal representation of those 8 bytes into it as plain text (lowercase, no spaces, e.g., `a1b2c3d4e5f60718`).

3. **Generate Summary (Redirection):**
   Write a bash script at `/home/user/pipeline.sh` that counts the number of lines in `corruption_report.txt` and the number of `.meta` files you created. 
   Output this as a JSON file to `/home/user/final_summary.json` with the exact keys: `"corrupt_records"` (integer) and `"new_meta_files"` (integer).

4. **Serve the Dataset:**
   Finally, start a background HTTP server serving the `/home/user/dataset_archive` directory on port `8080` using Python's built-in `http.server`. Save the PID of this background process to `/home/user/server.pid`.