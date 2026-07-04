You are a localization engineer managing translation strings for a global application. Our automated systems gather translation update logs from various regional servers. Previously, a bash pipeline was used to aggregate these CSV logs, but it silently dropped or corrupted rows where translators included embedded newlines in their text.

Your task is to build a robust, parallelized Python pipeline to process these translation logs.

The raw data is located in three directories simulating different regional servers:
- `/home/user/loc_servers/eu-west/updates.csv`
- `/home/user/loc_servers/us-east/updates.csv`
- `/home/user/loc_servers/ap-south/updates.csv`

Each CSV file has the following columns:
`timestamp,lang_code,original_text,translated_text`

Constraints and Requirements:
1. **Handle Embedded Newlines:** Use Python's `csv` module to properly parse the files. Some `translated_text` fields contain embedded newline characters (e.g., `\n`), which must be preserved exactly as they are.
2. **Timestamp Alignment:** The `timestamp` column contains times in various timezone offsets (e.g., `2023-11-01 14:30:00+02:00` or `2023-11-01 12:30:00Z`). You must parse these and convert them to a standardized UTC ISO 8601 string format: `YYYY-MM-DDTHH:MM:SSZ`.
3. **Parallel Processing:** You must process the CSV files in parallel using Python's `multiprocessing` or `concurrent.futures` module. 
4. **Data Aggregation and Sorting:** Aggregate all parsed records into a single list. Sort this unified list first by the standardized UTC `timestamp` (ascending), and then by `lang_code` (alphabetical).
5. **Output Format:** Write the sorted records to a JSON Lines file at `/home/user/compiled_locales.jsonl`. Each line must be a valid JSON object with the keys exactly as follows:
   `{"timestamp": "...", "lang_code": "...", "original_text": "...", "translated_text": "..."}`

Create a script named `/home/user/process_locales.py` that implements this pipeline and run it to produce the final `/home/user/compiled_locales.jsonl` file. Ensure the script completes successfully and handles all files gracefully.