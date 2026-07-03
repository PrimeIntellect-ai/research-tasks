You are a localization engineer tasked with updating translation memories and analyzing translator velocity for a software release. You will be working in `/home/user/loc_workspace`.

The task has four main parts: Local-Remote Data Transfer, Distance/Similarity Computation, Database Bulk Import/Export, and Windowed Aggregation.

**Phase 1: Local-Remote Transfer**
A local staging server is running at `http://localhost:8080`.
1. Download the file `http://localhost:8080/updates.tar.gz` and extract its contents into `/home/user/loc_workspace/updates/`.
This tarball contains two files: `new_strings.csv` and `translation_logs.csv`.

**Phase 2: Distance and Similarity Computation & Database Bulk Import**
You have an existing SQLite database at `/home/user/loc_workspace/translations.db` with a table `locales`:
`CREATE TABLE locales (id INTEGER PRIMARY KEY, en_source TEXT UNIQUE, es_target TEXT, fr_target TEXT);`

1. Write a Python script to process `new_strings.csv` (which has columns `en_source`, `es_target`, `fr_target`).
2. For each `en_source` in the CSV, compare it against ALL existing `en_source` strings currently in the `locales` database table using Python's `difflib.SequenceMatcher(None, string1, string2).ratio()`.
3. Find the maximum similarity ratio for each new string compared to the database strings.
4. **Fuzzy Matches:** If the maximum similarity ratio is $\ge 0.80$ and $< 1.0$, this indicates a fuzzy match (a minor string change). Do NOT insert these into the database. Instead, log them to `/home/user/loc_workspace/fuzzy_matches.csv` with the header `new_en_source,matched_db_en_source,similarity_ratio`. (If multiple DB strings tie for the max ratio, pick the one that comes first alphabetically. Round the ratio to 3 decimal places using Python's `round()`).
5. **Exact Matches & New Strings:** If the maximum similarity ratio is $< 0.80$ (completely new) OR exactly $1.0$ (exact match), insert or update the record in the `locales` table. If it's an exact match, update the `es_target` and `fr_target` to the new values from the CSV.
6. After processing all strings, bulk export the entire `locales` table to `/home/user/loc_workspace/final_export.json`. It must be a JSON array of objects, e.g., `[{"id": 1, "en_source": "...", "es_target": "...", "fr_target": "..."}]`.

**Phase 3: Windowed Aggregation**
The file `translation_logs.csv` contains logs of words translated per day with columns `date,translator_id,word_count`. The `date` format is `YYYY-MM-DD`.
1. Calculate a 3-day rolling sum of `word_count` for each `translator_id`. The 3-day window should include the current day and the two preceding calendar days. If there are days with missing logs for a translator, consider the word count as 0 for those days when calculating the sum.
2. Output the results to `/home/user/loc_workspace/rolling_stats.csv` with columns `date,translator_id,rolling_3d_sum`. Only include dates that appear in the original logs for that user. Order the output by `translator_id` ascending, then `date` ascending.

Complete all scripts and outputs within `/home/user/loc_workspace/`.