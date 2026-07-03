You are acting as a localization engineer. Our automated translation ETL job experienced network issues last week and retried multiple times, resulting in a large file containing duplicate, out-of-order, and unnormalized translation records. 

Your task is to build a Python data pipeline to clean, deduplicate, aggregate, and sample this data for human review, and finally "upload" it to a simulated remote directory.

The input file is located at `/home/user/translations_raw.jsonl`. Each line is a JSON object with the following schema:
- `timestamp`: ISO 8601 datetime (e.g., "2023-10-15T08:30:00Z")
- `context_key`: String identifier for the UI element
- `lang`: Target language code (e.g., "es", "ja", "ar")
- `source`: English source text
- `target`: Translated text (contains unnormalized Unicode characters)

Write a Python script (and any necessary shell commands) to perform the following operations:

1. **Unicode Normalization:** Normalize the `target` text of every record using the NFKC normalization form.
2. **Deduplication:** The ETL job created duplicate records for the same `context_key` and `lang`. Deduplicate the records by keeping ONLY the record with the most recent (latest) `timestamp`.
3. **Time-based Bucketing:** Add a new field called `month` to each preserved record, formatted as `YYYY-MM` (extracted from the timestamp).
4. **Stratified Sampling:** We need a sample for human review. Group the deduplicated dataset by `month` and `lang`. For each group:
   - Sort the records alphabetically by `context_key` (ascending).
   - Select the first `N` records, where `N = math.ceil(total_group_records * 0.2)`.
5. **Output Generation:** 
   - Save the fully deduplicated, normalized, and bucketed dataset to `/home/user/translations_dedup.jsonl`.
   - Save the sampled records to `/home/user/translations_review.jsonl`.
   - Ensure both files are valid JSONL, with JSON keys in the output sorted alphabetically.
6. **Simulated Remote Transfer:**
   - Compress both `.jsonl` files into a single archive named `/home/user/translations_archive.tar.gz`.
   - Create a directory `/home/user/remote_sync/` and copy the archive into it.

Requirements:
- Ensure your Python code processes the JSON lines efficiently.
- You must exactly follow the sampling rule (sort by `context_key` ascending, take `math.ceil(count * 0.2)`).