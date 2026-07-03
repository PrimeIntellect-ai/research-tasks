You are a localization engineer managing a continuous translation pipeline. Translation vendors drop JSON files containing localized strings into a designated directory. Your job is to build an automated ETL pipeline that validates these strings against the base English strings, imports the valid ones into a database, logs the invalid ones, and runs automatically on a schedule.

Here is the current system state:
- Base English strings: `/home/user/base_en.json`. Keys are string identifiers, values are English text which may contain placeholders like `{name}` or `{count}`.
- Drop directory: `/home/user/drops/`. Contains incoming translation files named by their language code (e.g., `es.json`, `fr.json`).
- Processed directory: `/home/user/processed/`.
- Database: `/home/user/loc_db.sqlite`. It has a table `translations (lang TEXT, key TEXT, text_val TEXT)`.

Write a Python script at `/home/user/etl_pipeline.py` that performs the following steps:
1. **Extract**: Read `/home/user/base_en.json` to determine all valid keys and their exact placeholders. Read all JSON files in `/home/user/drops/`.
2. **Validate**: For each translation key in a drop file:
   - Ensure the key exists in `base_en.json`.
   - Ensure the translated string contains *exactly* the same set of placeholders (e.g., `{name}`, `{count}`) as the base string. Placeholders are defined as any alphanumeric text surrounded by single curly braces.
3. **Transform & Load**: 
   - Bulk insert all *valid* translations into the `translations` table in `/home/user/loc_db.sqlite`. The `lang` column should be the filename without the `.json` extension (e.g., `es`).
   - For any *invalid* translation (missing/extra placeholders, or unknown key), append a line to `/home/user/invalid_translations.log` in this exact format: `<lang>.json:<key>:INVALID_PLACEHOLDERS`. (e.g., `es.json:welcome_msg:INVALID_PLACEHOLDERS`).
4. **Cleanup**: Move the processed files from `/home/user/drops/` to `/home/user/processed/`.

After writing the script, do the following:
1. Run the script once manually to process the current files in the drop directory.
2. Set up a cron job to run `/home/user/etl_pipeline.py` every 5 minutes. Save the crontab specification you apply into `/home/user/cron_backup.txt`.

Ensure your Python script uses standard libraries only (e.g., `sqlite3`, `json`, `re`, `shutil`, `os`).