You are acting as a localization engineer. We have received feedback logs from our European and North American servers containing user-submitted translation suggestions. Before these can be ingested into our central Translation Memory (TM) database, they must be processed, anonymized, and evaluated for similarity against our existing TM.

You need to write and execute a Python script to process these logs. 

**Input Files:**
1. `/home/user/inputs/server_eu.jsonl` - Contains JSON lines with fields: `time_local` (string with timezone offset, e.g., "2023-10-25 14:30:00+02:00"), `contact_email` (string), `ip_address` (string), and `suggested_translation` (string).
2. `/home/user/inputs/server_us.csv` - Contains columns: `epoch_time` (integer Unix timestamp), `user_ip` (string), `suggested_translation` (string).
3. `/home/user/inputs/tm_references.json` - A JSON dictionary where keys are translation IDs (e.g., "ref1") and values are reference translation strings.

**Requirements:**

1. **Timestamp Alignment:**
   Parse the timestamps from both log files and convert them to UTC. 
   Format the output timestamps as ISO 8601 strings ending with 'Z' (e.g., `2023-10-25T12:30:00Z`).

2. **Data Masking (PII):**
   You must redact any Personally Identifiable Information from the `suggested_translation` field.
   - Replace any email address (simple regex: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`) with the literal string `[EMAIL]`.
   - Replace any IPv4 address (regex: `\b(?:\d{1,3}\.){3}\d{1,3}\b`) with the literal string `[IP]`.

3. **Similarity Computation:**
   For each masked `suggested_translation`, calculate the similarity ratio against all reference strings in `/home/user/inputs/tm_references.json`. 
   Use Python's built-in `difflib.SequenceMatcher(None, masked_text, reference_text).ratio()`.
   Find the reference ID that yields the highest similarity score.

4. **Output Generation:**
   Create a single, unified JSONL output file at `/home/user/processed_translations.jsonl`.
   The file must be sorted chronologically by the new UTC timestamp from oldest to newest.
   Each line must be a JSON object with the following exact keys:
   - `timestamp_utc`: The aligned ISO 8601 timestamp (string).
   - `source`: The filename the record came from (`server_eu.jsonl` or `server_us.csv`).
   - `clean_text`: The masked suggested translation (string).
   - `best_match_id`: The key from `tm_references.json` that had the highest similarity score (string).
   - `similarity_score`: The highest similarity score rounded to 4 decimal places (float).

Write the script, execute it, and ensure the output file is generated correctly.