You are a localization engineer managing a translation pipeline. An upstream ETL job recently failed and retried automatically, which resulted in a massive dump of translation data with duplicate records. Furthermore, some of the retry records are missing confidence scores, and some translations contain unparsed placeholders.

You must write a Bash script named `/home/user/process_locales.sh` that processes a large data file (`/home/user/locales_etl_dump.csv`) in a memory-efficient way (e.g., using `awk`, `sed`, `sort`, and `bash` builtins - do not use Python, Ruby, or Perl for the data processing).

**Input Format:**
The file `/home/user/locales_etl_dump.csv` is a comma-separated file with the following columns:
`timestamp,string_id,locale,source_text,translated_text,confidence_score`
(Note: The file has no header row.)

**Processing Requirements:**
Your script must perform the following operations:

1. **Target Locale Streaming:** Process only rows where the `locale` is exactly `fr-FR`.
2. **Regex Filtering:** Drop any rows where the `translated_text` contains any sequence of 3 or more consecutive uppercase English letters (e.g., `ERROR`, `PLACEHOLDER`, `TXT`), as these indicate untranslated macros.
3. **Deduplication:** The ETL retry bug created duplicate `string_id`s for the same locale. For any duplicate `string_id`s within `fr-FR`, keep **only** the record with the highest `timestamp`. (Assume timestamps are integer Unix epochs).
4. **Chronological Sorting:** After deduplication, sort the remaining `fr-FR` records chronologically by `timestamp` (ascending).
5. **Imputation:** Some `confidence_score` values are blank (missing). You must impute these missing scores using **forward fill** (i.e., replace the missing score with the score from the immediately preceding chronological row). If the very first row is missing a score, use `50.0`. All scores are floats.
6. **Rolling Statistics:** Calculate a rolling average of the `confidence_score` (after imputation) over a window of the last 3 chronological records. (For the 1st record, the average is just its own score; for the 2nd, the average of the 1st and 2nd). Round the rolling average to exactly 2 decimal places.

**Output:**
The script must write the final processed data to `/home/user/fr_FR_rolling_stats.csv`.
The output format should be a CSV with the following columns:
`timestamp,string_id,confidence_score,rolling_avg`

Ensure your script `/home/user/process_locales.sh` is executable and runs without requiring arguments. Do not load the entire file into memory at once in pure Bash; rely on standard Unix stream processing utilities.