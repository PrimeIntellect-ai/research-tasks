You are a localization engineer managing community-submitted translation updates. You have received a bulk export of translation telemetry from the last few days. The data is in a JSON Lines format, but it contains raw, unaggregated submissions, some of which have encoding errors.

Your task is to process this data using Python to aggregate the best translations by language and day.

**Input Data:**
File: `/home/user/loc_drop/raw_telemetry.jsonl`
Format: Each line is a JSON object with the following keys:
- `ts`: ISO 8601 timestamp (e.g., "2023-10-14T15:30:00Z")
- `lang`: Language code (e.g., "ja-JP", "ar-SA")
- `str_id`: The unique identifier for the localized string (e.g., "ui.button.save")
- `text`: The proposed translation string (contains UTF-8 characters, emojis, and potentially RTL text)
- `score`: User trust score (integer)

**Processing Requirements:**
1. **Filtering:** Discard any record where the `text` field contains the Unicode replacement character (`\ufffd`). These represent corrupted submissions.
2. **Time Bucketing:** Group the submissions by their calendar date (YYYY-MM-DD) based on the `ts` field.
3. **Grouping & Aggregation:** For each distinct `lang` and `date` bucket, determine the "best" translation for each `str_id`. 
   - The "best" translation is the one with the highest `score`.
   - If there is a tie in `score`, prefer the translation with the *earliest* timestamp (`ts`).
4. **Output Generation:** 
   - Create a directory `/home/user/loc_drop/aggregated/`.
   - For each language and date bucket that has valid records, output a tab-separated values (TSV) file named exactly `{lang}_{date}.tsv` (e.g., `ja-JP_2023-10-14.tsv`).
   - Each TSV file must contain three columns: `str_id`, `text`, and `score`. No header row.
   - The rows inside each TSV file must be sorted alphabetically by `str_id`.
   - Ensure the output files are encoded in UTF-8.

Write and execute a Python script to perform this data processing pipeline.