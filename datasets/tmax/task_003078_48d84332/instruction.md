You are a data analyst working with a corrupted timeseries dataset from international IoT sensors. The CSV data contains broken Unicode escape sequences, duplicate messages, and missing time intervals.

Your task is to write a C program that cleans, deduplicates, and resamples this data.

**Requirements:**

1.  **Input Data:**
    Read the CSV file located at `/home/user/input.csv`.
    The CSV has no header. The format is: `timestamp,message,reading`
    - `timestamp`: Unix epoch time (integer). The file is sorted by timestamp.
    - `message`: A string that may contain standard ASCII and broken JSON-style Unicode escapes (e.g., `\u00e9` for `é`).
    - `reading`: A floating-point number.

2.  **Unicode Normalization:**
    As you read each row, you must parse the `message` field and convert any `\uXXXX` escape sequences into standard UTF-8 encoded bytes. (Assume all `XXXX` are valid hex codes in the Basic Multilingual Plane).

3.  **Hash-Based Deduplication:**
    You must maintain a history of all normalized messages you have seen.
    Use the `djb2` hash function to hash the *normalized* UTF-8 message.
    If a row contains a normalized message that has already appeared in *any* previous valid row, the current row is considered a duplicate and must be completely ignored.

4.  **Resampling and Gap-Filling:**
    The output must represent a continuous timeseries with exactly one data point every 60 seconds.
    - Let `T0` be the timestamp of the *first valid (non-duplicate) row* in the file.
    - Your time buckets will be `[T0, T0+60)`, `[T0+60, T0+120)`, etc.
    - For each 60-second bucket, evaluate all valid input rows whose timestamps fall within that bucket.
    - **If the bucket has valid rows:** The output for this bucket will use the `reading` and `normalized message` of the *latest* valid row within that bucket (the one with the highest timestamp).
    - **If the bucket has no valid rows (a gap):** Forward-fill the data. Use the `reading` and `normalized message` from the *previous* bucket.
    - The timestamp written to the output for a bucket must be the *start time* of that bucket (e.g., `T0`, `T0+60`).
    - Stop generating output after producing the bucket that contains the timestamp of the *last valid row* in the entire input file.

5.  **Output Format:**
    Write the processed data to `/home/user/output.csv`.
    Format: `bucket_start_timestamp,normalized_message,reading`
    Ensure readings are printed to exactly 2 decimal places (e.g., `%.2f`).

**Constraints:**
- Use **C** to write the processing program (e.g., `/home/user/process.c`).
- Compile it with standard `gcc` (e.g., `gcc -O3 /home/user/process.c -o /home/user/process`).
- You may use any standard C library functions (`stdio.h`, `stdlib.h`, `string.h`, etc.).
- Ensure your output file exactly matches the expected format.

Run your compiled C program to generate `/home/user/output.csv` so it can be automatically verified.