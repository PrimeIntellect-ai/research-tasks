You are a localization engineer managing translation strings for a software project. You have received an automated export of new translations in JSON-Lines format, but the exporter had a bug that produced truncated or invalid unicode escape sequences (e.g., `\u00` instead of `\u0000`, or `\uZZZZ`), causing standard JSON parsers to break.

Your task is to build a Python data pipeline to clean, reshape, and enrich this data. Create a script at `/home/user/process_locales.py` that performs the following steps:

1. **Pipeline Logging:** Configure standard logging to write to `/home/user/pipeline.log`. Log a message at the start ("Pipeline started") and end ("Pipeline finished") of your script.
2. **Sanitize and Parse:** Read `/home/user/raw_translations.jsonl`. Before parsing each line with `json.loads()`, use regex to remove any invalid unicode escape sequences. Specifically, remove any literal `\u` that is NOT followed by exactly 4 valid hexadecimal digits (0-9, a-f, A-F). Do not remove the surrounding characters, just the invalid `\u` and any immediate hex digits up to 3 characters if they were part of the invalid escape sequence (e.g., `\u00` should be removed, `\uZZZZ` should have the `\u` removed, leaving `ZZZZ`).
3. **Reshape (Wide to Long):** Convert the parsed JSON data into a pandas DataFrame. The data is currently in a "wide" format (keys: `term`, `es`, `fr`, `de`). Reshape it into a "long" format with three columns: `term`, `lang`, and `translation`.
4. **Merge:** Join the reshaped DataFrame with the glossary categories provided in `/home/user/categories.csv` using an inner join on the `term` column.
5. **Normalization:** Standardize the `translation` column by converting all strings to lowercase and stripping any leading or trailing whitespace.
6. **Rolling Aggregation:** Sort the DataFrame primarily by `category` (ascending), then `term` (ascending), and finally `lang` (ascending). Then, within each `category` group, calculate the rolling average of the length of the `translation` strings using a window size of 2 and `min_periods=1`. Store this in a new column named `rolling_len_avg`.
7. **Output:** Save the resulting DataFrame to `/home/user/final_locales.csv` (include headers, do not include the index).

You must write and execute this script to complete the task.