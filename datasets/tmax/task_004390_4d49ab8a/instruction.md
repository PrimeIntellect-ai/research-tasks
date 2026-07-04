You are a localization engineer managing a continuous influx of translation updates. Freelance translators submit strings at various times, and these submissions are logged in a time-series CSV file. Over time, the log accumulates millions of rows, including corrections (newer timestamps for the same translation key), invalid data, and formatting inconsistencies.

Your task is to write a Go program that processes a large time-series CSV file of translation submissions, cleans and validates the data, and extracts the most recent valid translation for each key and language.

**Input File:**
`/home/user/raw_translations.csv`
Headers: `timestamp,translator_id,lang_code,translation_key,translated_text`

**Requirements for your Go program:**
1. **Streaming:** You must process the CSV file efficiently (e.g., using `encoding/csv` in a stream) as it could theoretically be larger than available memory.
2. **Normalization:** Convert all `lang_code` values to lowercase (e.g., `EN-US` becomes `en-us`).
3. **Validation Constraints:** 
   A row is considered **invalid** if it fails *any* of the following checks:
   - `timestamp` must be a valid RFC3339 formatted time.
   - The normalized `lang_code` must be exactly one of: `en-us`, `fr-fr`, `es-es`, `de-de`, `ja-jp`.
   - `translator_id` must be a valid integer.
   - `translation_key` must not be empty.
   - `translated_text` must not be empty.
4. **Invalid Row Handling:** Write any invalid rows (exactly as they appeared in the input, including original case, without headers) to `/home/user/invalid_rows.csv`.
5. **Deduplication:** For the *valid* rows, you must resolve multiple submissions for the same `(normalized lang_code, translation_key)` pair. Keep ONLY the translation with the most recent (latest) `timestamp`. If timestamps are exactly identical, keep the first one encountered in the file.
6. **Output:** Write the final, deduplicated valid translations to `/home/user/latest_translations.jsonl`. 
   - Each line must be a valid JSON object with the keys: `timestamp` (string), `translator_id` (integer), `lang_code` (string, normalized), `translation_key` (string), and `translated_text` (string).
   - The output lines in the JSONL file **must be sorted** alphabetically by `lang_code`, and then alphabetically by `translation_key`.

Write your Go code in `/home/user/process_translations.go`, compile it, and run it to produce the output files.