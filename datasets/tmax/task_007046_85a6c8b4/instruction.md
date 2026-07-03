You are a localization engineer managing a translation pipeline. You receive daily batches of translated strings, but the upstream translation service occasionally produces broken JSON-Lines files with malformed unicode escape sequences. 

Your task is to process a new batch of translations, merge them into the master Translation Memory (TM), and generate a sample for Quality Assurance (QA).

You have the following inputs:
1. Master TM: `/home/user/tm_master.csv` (Columns: `string_id`, `en_source`, `locale`, `translation`)
2. Incoming batch: `/home/user/incoming/batch_01.jsonl` (Format per line: `{"en": "...", "locale": "...", "trans": "..."}`)

Write a Python script (or use bash/Python combinations) to perform the following pipeline:

**Step 1: Robust Parsing & Error Handling**
Read `/home/user/incoming/batch_01.jsonl` line by line. Some lines contain malformed unicode escapes (e.g., `\u00Z` or cut off) which will raise a `json.decoder.JSONDecodeError` if you try to parse them with standard `json.loads`.
- Catch these exceptions.
- Write the exact raw, unparsed string lines that failed to parse into `/home/user/errors.log` (one per line, keeping the original line endings).
- Keep only the successfully parsed JSON objects for the next step.

**Step 2: Hash-Based Deduplication & Merge**
For the successfully parsed incoming translations:
- Calculate a `string_id` for each row using the standard MD5 hex digest of the English source string (`en`).
- A translation is considered a "duplicate" if the `(string_id, locale)` pair already exists in `/home/user/tm_master.csv`.
- Append only the **new, non-duplicate** translations to `/home/user/tm_master.csv`. Keep the CSV format identical (columns: `string_id,en_source,locale,translation`). 

**Step 3: Stratified QA Sampling**
From the **newly added translations only** (do not include original TM rows), extract a QA sample.
- For each `locale` present in the newly added strings, select exactly 2 strings. If a locale has fewer than 2 new strings, select all of them.
- To make this deterministic: for each locale, sort the new strings alphabetically by their MD5 `string_id` and pick the first 2.
- Write this sample to `/home/user/qa_sample.csv` with the headers: `locale,string_id,translation`.
- The rows in `qa_sample.csv` should be sorted alphabetically by `locale`, and then alphabetically by `string_id`.

Ensure all output files are placed exactly at the specified paths.