You are a localization data engineer. We have a daily batch of translation engagement metrics and a localization dictionary that need to be merged and transformed into a time-series report. A previous bash-based pipeline was silently dropping string mappings because of embedded newlines in the translated text. 

Your task is to write a robust Python script `/home/user/process_metrics.py` and run it to produce a clean, reshaped CSV report.

**Input Files:**
1. `/home/user/metrics.csv` (Long-format time-series)
   - Columns: `timestamp`, `string_id`, `locale`, `clicks`
   - `timestamp` is in ISO 8601 format (e.g., `2023-10-01T14:32:01Z`).
   - `clicks` is an integer.

2. `/home/user/translations.csv` (Localization dictionary)
   - Columns: `string_id`, `locale`, `translation_text`
   - **Warning:** `translation_text` fields contain embedded newlines and commas (properly quoted per RFC 4180).

**Processing Requirements:**
1. **Normalization:** Convert the `timestamp` in `metrics.csv` to a simple date format `YYYY-MM-DD` (e.g., `2023-10-01`).
2. **Quality Gates & Validation (Constraints):**
   - Drop any rows in `metrics.csv` where `clicks < 0` (these are logging errors).
   - Inner join the valid metrics with `translations.csv` on `string_id` AND `locale`. If a metric does not have a matching translation in the dictionary, drop it.
3. **Aggregation:** Calculate the sum of valid `clicks` per `date` and `locale`.
4. **Reshaping (Long to Wide):**
   - Pivot the aggregated data so that each row represents a single `date`, and each column represents a `locale`.
   - The output columns must be: `date`, followed by all unique locales found in the validated data, sorted alphabetically (e.g., `date`, `de_DE`, `en_US`, `es_ES`, `ja_JP`).
   - If a locale has no clicks on a specific date, fill the missing value with `0`.
   - Sort the final output chronologically by `date` ascending.

**Output:**
Save the final reshaped dataset to `/home/user/daily_locale_clicks.csv`.

Ensure you run your Python script so the output file is generated. Do not leave the task until `/home/user/daily_locale_clicks.csv` exists and is perfectly formatted.