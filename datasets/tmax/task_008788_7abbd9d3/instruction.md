You are a localization engineer managing a translation pipeline. You have received a raw translation dump in `/home/user/raw_locales.csv`. This file is in long format with the columns: `timestamp`, `msg_id`, `locale`, `translation`. Note that some `translation` fields contain embedded newlines.

Write a Python script `/home/user/process.py` to clean, reshape, and summarize this data. Your script must perform the following operations:

1. **Read the CSV safely**: Ensure embedded newlines in the `translation` column are parsed correctly.
2. **Latest Timestamp Deduplication**: If multiple records exist for the same `(msg_id, locale)` combination, keep only the record with the most recent `timestamp` (lexicographical string comparison on the ISO8601 timestamp is sufficient).
3. **Hash-based Translation Deduplication**: Sometimes translators provide the exact same text for different message IDs in the same locale. Within each `locale`, compute the MD5 hash of the `translation` string. If multiple records share the same MD5 hash (meaning the translation text is exactly identical), keep only the record with the lexicographically smallest `msg_id`. Drop the others for that locale.
4. **Wide-format Reshaping**: Reshape the cleaned records into a wide format, where each row represents a unique `msg_id`, and the columns represent the locales.
5. **Filter**: Drop any `msg_id` that does not have an `en` (English) translation after the deduplication steps.
6. **Save Wide CSV**: Export the reshaped data to `/home/user/wide_locales.csv`. The columns must be `msg_id`, followed by all available locales sorted alphabetically (e.g., `msg_id, en, es`). Rows must be sorted alphabetically by `msg_id`. Fill missing translations with an empty string.
7. **Time-based Bucketing & Reporting**: For each remaining `msg_id`, determine its "month bucket" based on the `timestamp` of its `en` translation (format `YYYY-MM`). Group the `msg_id`s by this month bucket.
8. **Template Generation**: For each month bucket, generate a report file named `/home/user/report_{YYYY-MM}.txt` using exactly this format:
```
Month: {YYYY-MM}
Messages: {number of msg_ids in this month}
```

Run your script to produce the required files.