You are an automation specialist tasked with building a robust data processing workflow for a fleet of IoT temperature sensors. We receive time-series data in various formats, but our streams have recently been targeted by malformed data injections designed to crash our downstream aggregators and databases.

Your task is to build a two-part solution:

**Part 1: The Data Sanitizer / Classifier**
Create a Python script at `/home/user/verify_stream.py` that acts as a strict gatekeeper. 
It must accept a file path via a `--input` argument. The script must parse the file (which will be a CSV, potentially in various character encodings like UTF-8, UTF-16, or Windows-1252) and validate every row. 

A file is considered "CLEAN" and the script must exit with status code `0` if AND ONLY IF all rows meet these conditions:
1. `timestamp`: Must be a valid ISO8601 string representing a date between January 1, 2000, and December 31, 2050.
2. `sensor_id`: Must be strictly alphanumeric (regex `^[A-Za-z0-9]+$`). No spaces, punctuation, or special characters.
3. `temperature`: Must be a valid float between `-100.0` and `200.0` inclusive.
4. The file must be readable without encoding replacement errors (i.e., no corrupted bytes disguised as valid text).

If the file contains ANY row that violates these rules (e.g., SQL injection attempts in `sensor_id`, out-of-bounds temperatures, malformed timestamps, or garbage encoding), the file is considered "EVIL" and the script must immediately exit with status code `1`.

**Part 2: The Aggregation Pipeline**
Create a script at `/home/user/pipeline.py`. This script will process a directory of mixed-format files:
- Standard CSVs and Parquet files containing `timestamp`, `sensor_id`, and `temperature`.
- Proprietary binary blobs (`.dat` files). 

There is a legacy, stripped binary tool located at `/app/decoder`. We don't have the source code for it, but it converts `.dat` files into standard CSVs. You will need to reverse-engineer its CLI usage (e.g., by running it or inspecting it) to extract the binary data in your pipeline.

For every file in a target directory:
1. Decode/Read the data (handling encodings safely).
2. Filter out any invalid rows (using the logic from Part 1).
3. Compute a 15-minute rolling average of the `temperature` for each `sensor_id`, ordered by `timestamp`.
4. Perform a bulk export/insert of the resulting cleaned, aggregated time-series data into a SQLite database at `/home/user/metrics.db` in a table named `rolling_temps` (columns: `sensor_id`, `window_end_time`, `avg_temperature`).

We will test your `verify_stream.py` against a hidden corpus of clean and evil files.