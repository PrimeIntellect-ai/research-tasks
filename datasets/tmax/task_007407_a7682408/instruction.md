You are an AI assistant helping a scientific researcher organize and back up a set of proprietary experimental data files. 

The researcher has a folder of raw data files located at `/home/user/dataset/raw/`. Each file is a custom binary-text hybrid format with a `.dat` extension. 
There is also a backup folder at `/home/user/dataset/backup/` which contains an existing manifest file `manifest.jsonl` and some previously backed-up `.dat` files.

**File Format Specification:**
Each `.dat` file starts with a 12-byte binary header:
- Bytes 0-3: Magic string `RSCH` (ASCII)
- Bytes 4-7: Timestamp (32-bit unsigned integer, little-endian)
- Bytes 8-9: Format Version (16-bit unsigned integer, little-endian)
- Bytes 10-11: Header Length (16-bit unsigned integer, little-endian, always 12)

Immediately following the 12-byte header is a plain-text CSV payload. The CSV always has a header row: `record_id,sensor_value,status`.
- `sensor_value` is a floating-point number.

**Your Objectives:**

1. **Write a C program (`/home/user/extractor.c`):**
   Write and compile a C program named `extractor` that takes a single file path as a command-line argument.
   The program must:
   - Calculate the SHA256 checksum of the *entire* raw file. (You may use external commands via `popen` or libraries like OpenSSL for the hashing, but the extraction must be in C).
   - Read the binary header and extract the Timestamp.
   - Read the CSV payload and calculate the arithmetic mean (average) of all the `sensor_value` entries.
   - Print exactly one line to standard output in valid JSON format containing the extracted data:
     `{"file": "<basename_of_file>", "sha256": "<checksum>", "timestamp": <timestamp_int>, "avg": <average_float_rounded_to_2_decimal_places>}`

2. **Write an incremental backup script (`/home/user/backup.sh`):**
   Write a bash script that processes all `.dat` files in `/home/user/dataset/raw/`.
   For each file, use your compiled `extractor` program to generate the JSON record.
   The script must implement an incremental backup:
   - Check if the SHA256 checksum of the file already exists anywhere in `/home/user/dataset/backup/manifest.jsonl`.
   - If the checksum is NOT in the manifest, copy the `.dat` file to `/home/user/dataset/backup/` and append the JSON record produced by the C program to `/home/user/dataset/backup/manifest.jsonl`.
   - If the checksum IS already in the manifest, skip the file (do not copy, do not append to manifest).

3. **Execute the workflow:**
   Compile your C program, run the `backup.sh` script, and ensure the backup folder and manifest are successfully updated with the new files.