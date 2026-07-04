You are a localization engineer managing translation strings for a global application. Your automated systems have dumped a large JSON-lines log of translation updates into `/home/user/raw_translations.jsonl`. 

Due to a bug in the upstream logging pipeline, the `text` field contains double-escaped unicode sequences (e.g., `\\u00e1` instead of the actual `á` character) which breaks downstream naive parsers. 

Your task is to write a Bash-based data processing pipeline (you may use standard tools like `jq`, `awk`, `sed`, `xargs`, `parallel`, etc.) that accomplishes the following:

1. **Clean & Normalize**: Convert all double-escaped unicode sequences (like `\\uXXXX`) in the `text` field into their actual UTF-8 characters.
2. **Parallel Processing**: Split and process the data by the `locale` field in parallel.
3. **Deduplication**: There are multiple updates for the same `string_id` and `locale`. For each `locale` and `string_id`, keep ONLY the entry with the highest `timestamp`.
4. **Structured Output**: Save the normalized, deduplicated valid JSON-lines for each locale in `/home/user/processed/<locale>.jsonl`. The entries inside each file MUST be sorted by `timestamp` in ascending order.
5. **Rolling Statistics**: For the `es-ES` locale only, compute a 3-item rolling average of the string length (number of UTF-8 characters, NOT bytes) of the normalized `text` field, ordered by timestamp ascending. 
   - Calculate the average using up to the last 3 available entries (e.g., Row 1: avg(Row 1), Row 2: avg(Row 1, Row 2), Row 3: avg(Row 1..3), Row 4: avg(Row 2..4)).
   - Save these averages to `/home/user/es-ES_rolling_avg.txt`, one number per line, rounded to exactly 1 decimal place.

**Data Format**:
The input `/home/user/raw_translations.jsonl` has the format:
`{"timestamp": <unix_timestamp>, "string_id": "<id>", "locale": "<locale>", "text": "<text>"}`

**Requirements**:
- Create the `/home/user/processed/` directory.
- Do not lose or modify any JSON keys.
- Ensure the final JSON files contain actual UTF-8 characters, not `\uXXXX` escapes.