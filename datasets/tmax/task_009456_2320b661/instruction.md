You are a localization engineer tasked with processing a batch of crowdsourced translation updates. You have received a raw data file at `/home/user/raw_translations.csv`. 

You must write a Go program (`/home/user/process_loc.go`) that performs the following data processing pipeline:

1. **Read and Validate:**
   Read the CSV file which has headers: `timestamp,lang_code,translation_key,original_text,translated_text`.
   Validate each row according to these strict rules:
   - `lang_code` must match the regex: `^[a-z]{2}(-[A-Z]{2})?$` (e.g., `en`, `fr-CA`).
   - `translation_key` must match the regex: `^[a-zA-Z0-9_]+$`.
   - **Placeholder matching:** Any substring enclosed in curly braces (e.g., `{name}`) present in the `original_text` MUST also appear exactly in the `translated_text`, and vice versa. If there is a mismatch in placeholders, the string is invalid.

2. **Error Logging:**
   Write the raw CSV line (exactly as it appears in the input, without a trailing newline if it's the last line, but typical Unix line endings otherwise) of every *invalid* row to `/home/user/invalid_strings.log`.

3. **Sorting, Grouping, and Rolling Statistics:**
   For the *valid* rows, process them chronologically (sorted by `timestamp` ascending).
   For each `lang_code`, maintain a rolling cumulative average of the "expansion ratio". 
   - `expansion_ratio` = (character length of `translated_text`) / (character length of `original_text`).
   - The rolling cumulative average is the average of the expansion ratios of all valid translations processed *so far* for that specific `lang_code`.

4. **Database Export:**
   Create an SQLite database at `/home/user/translations.db`.
   Create a table named `translations` with the schema:
   `CREATE TABLE translations (lang_code TEXT, translation_key TEXT, original_text TEXT, translated_text TEXT, rolling_avg_ratio REAL, PRIMARY KEY (lang_code, translation_key));`
   Insert the valid translations into this database. Because there may be multiple updates for the same `translation_key` and `lang_code`, you must only keep the **latest** valid translation (based on `timestamp`). The `rolling_avg_ratio` saved should be the cumulative average calculated at the moment that specific translation was processed.

**Instructions for the AI:**
- Initialize a Go module (`go mod init loc`) in `/home/user`.
- You may use `github.com/mattn/go-sqlite3` for database operations.
- Build and run your Go program to produce the final `invalid_strings.log` and `translations.db` files.