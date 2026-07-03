You are acting as a localization engineer updating translation datasets for a multimedia application. We need you to build a robust data processing pipeline that standardizes incoming localization files and strictly filters out corrupted or malicious submissions.

First, there is a reference audio file located at `/app/localization/reference_sync.wav`. This audio contains a spoken sequence of three synchronization markers: "Sync one", "Sync two", and "Sync three". You will need to transcribe this audio to determine the exact timestamp (in seconds) of each sync marker.

Second, you must create a Python script at `/home/user/sanitize_loc.py` that acts as a strict filter and formatter for incoming translation CSV files. The script must take a single command-line argument (the path to a CSV file) and do the following:

1. **Wide-Long Format Reshaping**: The input CSVs are in a wide format with columns: `key`, `timestamp`, `en`, `es`, `fr`, `de`. You must reshape this data into a long format with columns: `key`, `timestamp`, `language`, `translation`.
2. **Timestamp Alignment**: The `timestamp` column in the input CSV represents raw sync points (0, 1, and 2). You must map these to the actual audio timestamps (in seconds) you found in `/app/localization/reference_sync.wav` corresponding to "Sync one", "Sync two", and "Sync three", respectively.
3. **Normalization**: All `key` values must be converted to lowercase and spaces replaced with underscores.
4. **Validation and Filtering**: The script must validate the data. It must REJECT the file (exit with code 1) if:
   - Any translation string contains malicious HTML/JS tags (e.g., `<script>`, `onload=`).
   - The original CSV contains rows where any of the language columns (`en`, `es`, `fr`, `de`) are completely empty or missing.
   - The raw timestamps are anything other than `0`, `1`, or `2`.
   If the file passes all checks, the script must print the reshaped, aligned, and normalized long-format CSV to `stdout` and ACCEPT the file (exit with code 0).

To help you develop and test your script, we have provided two corpora of test files:
- `/app/corpora/clean/`: Contains perfectly valid translation CSVs. Your script must exit 0 for all these files.
- `/app/corpora/evil/`: Contains CSVs with various issues (XSS payloads, missing columns, invalid timestamps). Your script must exit 1 for all these files.

Please create the `/home/user/sanitize_loc.py` script so that it correctly passes the adversarial test suite (accepting 100% of the clean corpus and rejecting 100% of the evil corpus) while performing the required transformations.