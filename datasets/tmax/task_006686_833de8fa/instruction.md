You are a localization engineer managing translation strings for a software project. You need to process incoming translation updates from a vendor, clean them, validate them against existing source text, and update the project's SQLite database.

Your workspace is `/home/user`.

1. **Database Setup**: 
   There is an existing SQLite database at `/home/user/translations.db`. 
   It has a table named `strings` with the following schema:
   `id INTEGER PRIMARY KEY, lang TEXT, string_key TEXT, source_text TEXT, translated_text TEXT, updated_at TEXT`
   This database contains the master copy of all translations.

2. **Incoming Data**:
   You have received an incoming CSV file from a translation vendor at `/home/user/vendor_updates.csv`.
   The CSV has the following columns: `lang, string_key, translation, timestamp`

3. **Your Task**:
   Write and execute a Python script to process `vendor_updates.csv` and update `translations.db` following these exact requirements:

   **Phase 1: Cleaning & Deduplication**
   - Read the CSV.
   - Trim leading and trailing whitespace from the `translation` field.
   - Deduplicate entries: If there are multiple rows with the exact same `lang` and `string_key`, strictly keep only the one with the latest `timestamp` (lexicographical string comparison is fine for ISO 8601 timestamps). Discard the older ones *before* validation.

   **Phase 2: Validation**
   For each deduplicated, cleaned translation update, validate it against these constraints. You will need to look up the `source_text` for the corresponding `lang` and `string_key` in the `translations.db` to perform these checks.
   - **Constraint A**: The cleaned `translation` must not be empty.
   - **Constraint B**: The database must already have a record for this `lang` and `string_key`. You cannot insert entirely new keys or languages; you are only updating existing records.
   - **Constraint C**: The number of `%s` placeholders in the `translation` must exactly match the number of `%s` placeholders in the `source_text`.

   **Phase 3: Database Update & Logging**
   - For every update that **passes** all validation constraints: Update the `translated_text` and `updated_at` fields in the `translations.db` `strings` table. Use the `timestamp` from the CSV as the new `updated_at` value.
   - For every update that **fails** validation: Do not update the database. Instead, log the failure.

   **Output File**:
   Create a JSON file at `/home/user/validation_errors.json` containing a list of objects for all rejected updates (including those ignored because the key didn't exist). 
   The list must be sorted alphabetically by `lang`, then by `string_key`.
   The format should be exactly:
   ```json
   [
     {
       "lang": "es",
       "string_key": "greeting",
       "reason": "placeholder_mismatch"
     },
     {
       "lang": "fr",
       "string_key": "btn_cancel",
       "reason": "empty_string"
     },
     {
       "lang": "ru",
       "string_key": "unknown_key",
       "reason": "not_in_db"
     }
   ]
   ```
   *Note: Use the exact reason strings: `empty_string`, `not_in_db`, or `placeholder_mismatch`. If a translation fails multiple constraints, report `not_in_db` as priority 1, `empty_string` as priority 2, and `placeholder_mismatch` as priority 3.*