You are a localization engineer tasked with cleaning up a messy file of crowd-sourced translations and importing them into our local SQLite database for the translation service.

You have a raw CSV file located at `/home/user/raw_translations.csv` with the following columns: `key`, `lang`, `translation`.

The translations suffer from formatting inconsistencies. You must write a Go program at `/home/user/clean_i18n.go` that reads this CSV and writes a cleaned version to `/home/user/cleaned.csv` according to the following normalization rules:
1. **Whitespace Normalization:** Trim all leading and trailing whitespaces from the `translation` column. Also, replace any occurrence of two or more consecutive spaces within the translation with a single space.
2. **Placeholder Standardization:** Translators have used different placeholder formats, including `{param}`, `{{param}}`, and `[param]` (where `param` can be any combination of alphanumeric characters and underscores). Use a Regular Expression to find all these placeholders and replace them entirely with the exact standard string `{{VAR}}`.

After writing and running your Go script to produce `/home/user/cleaned.csv`, use standard shell tools (specifically `sqlite3`) to:
1. Create a new SQLite database at `/home/user/locales.db`.
2. Create a table named `translations` with the schema: `key TEXT, lang TEXT, translation TEXT`.
3. Bulk import the data from `/home/user/cleaned.csv` into the `translations` table. Ensure the CSV header row is properly skipped or excluded from the final table data.

Your final deliverable is the populated SQLite database at `/home/user/locales.db`.