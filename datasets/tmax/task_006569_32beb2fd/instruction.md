You are tasked with building a custom Configuration Manager Tracker in Python that processes changed configuration files, extracts specific identifiers, compresses them using a custom algorithm, and safely logs them to a central archive.

Write a Python script at `/home/user/tracker.py` that fulfills the following requirements:

1. **Configuration Interpretation:**
   The script must first read its own configuration from `/home/user/tracker.ini` (which already exists). It should parse this INI file to find the output archive path located under the `[Settings]` section, key `archive_path`.

2. **Standard Stream Processing:**
   The script must accept a list of absolute file paths via standard input (`stdin`), with one file path per line.

3. **Structured Format Parsing:**
   For each file path received, determine its type by the extension and extract the configuration hash:
   - If it is a `.json` file: Parse it as JSON and extract the value of the `config_hash` key.
   - If it is a `.csv` file: Parse it as a CSV (with headers). Extract the value of the `hash` column from the first data row.

4. **Custom Compression:**
   Compress the extracted hash string using a custom Run-Length Encoding (RLE) format. 
   - Rule: Replace consecutive identical characters with the count of those characters followed by the character itself.
   - Example 1: `AABBBCCCC` becomes `2A3B4C`
   - Example 2: `X` becomes `1X`
   - Example 3: `11122333` becomes `312233`

5. **File Locking and Output:**
   For each processed file, the script must:
   - Open the target archive file (from the INI config) in append mode.
   - Acquire an exclusive file lock on the archive file using `fcntl.flock` to ensure thread/process safety (as multiple trackers might run concurrently in production).
   - Write a single line to the archive file in the format: `<basename_of_file>:<compressed_hash>\n` (e.g., `app.json:2A3B4C`).
   - Release the lock and close the file.

Once your script is complete, test it by piping the files located in `/home/user/data/` into your script. 
Specifically, run:
`find /home/user/data -type f | python3 /home/user/tracker.py`

*Note: The system has standard Python 3.x libraries available. Do not use external libraries (like pandas) for this task.*