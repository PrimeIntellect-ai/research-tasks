You are acting as a localization engineer. You need to build a data processing pipeline to handle a stream of updated translation strings from translators. The incoming data is provided as a JSON-Lines (JSONL) file, but it contains malformed unicode escape sequences that break standard JSON parsers.

Your pipeline must download the data, clean it, apply validation checks, deduplicate updates, and compute rolling text-length statistics.

**Setup Instructions:**
1. Create a working directory at `/home/user/loc_pipeline`.
2. The raw data is hosted on a local server. Write a Python script to download the file from `http://127.0.0.1:8000/raw_translations.jsonl` (you will need to start a temporary local server in the background using `python3 -m http.server 8000` in the directory where you create the raw file, but for the sake of this task, I will provide the data generation script below. Wait, the system will actually provide the server. Assume the server is already running and serving the file at that URL).
*Correction: Actually, to ensure the environment is fully self-contained, you must first write the raw data to `/home/user/server/raw_translations.jsonl`, start `python3 -m http.server 8000` in `/home/user/server/` as a background process, and then write your pipeline to fetch from `http://127.0.0.1:8000/raw_translations.jsonl`.*

**Data Processing Pipeline Requirements (`/home/user/loc_pipeline/pipeline.py`):**
Write a Python script that fetches the raw JSONL file and processes it row by row or as a batch with the following steps:

1. **Cleaning (Malformed Unicode):**
   The raw file has literal invalid unicode escape sequences. Specifically, standard JSON requires `\u` to be followed by exactly 4 hexadecimal digits. Some strings in the file contain `\u` followed by 4 characters where one or more are NOT valid hex digits (e.g., `\u00qs`).
   * Before parsing each line as JSON, you must use a regular expression to find any `\u` followed by exactly 4 characters that are *not* a valid 4-hex-digit sequence. Replace the entire 6-character sequence (e.g., `\u00qs`) with the standard Unicode replacement character sequence `\uFFFD`.
   * After this text-level replacement, parse the line as JSON.

2. **Validation Checkpoint:**
   Drop any parsed JSON record where the `lang` field is not exactly two lowercase letters (e.g., keep "en", drop "eng" or "EN").

3. **Deduplication:**
   Records have the fields: `id` (string), `lang` (string), `text` (string), and `timestamp` (integer).
   If multiple records have the same `id` and `lang`, keep ONLY the record with the strictly highest `timestamp`. Drop the older versions.

4. **Rolling Aggregation:**
   After deduplication, sort the remaining valid records globally by `timestamp` in ascending order.
   For each `lang`, compute a rolling average of the character length of the `text` field (after JSON decoding, so `\uFFFD` counts as 1 character).
   * The rolling window size is 3. This means the average is based on the current record's text length and up to 2 previous records' text lengths *for that specific language*.
   * Round the rolling average to exactly 2 decimal places.

5. **Outputs:**
   Your script must produce two files in `/home/user/loc_pipeline/`:
   * `clean_translations.jsonl`: The deduplicated, sorted (by timestamp asc) valid JSON records.
   * `rolling_stats.csv`: A CSV file with the columns `timestamp,lang,id,text_length,rolling_avg_len`, ordered exactly matching the sorted valid records.

**Execution:**
Start the background server, run your pipeline, and ensure the output files are correctly generated in `/home/user/loc_pipeline/`.