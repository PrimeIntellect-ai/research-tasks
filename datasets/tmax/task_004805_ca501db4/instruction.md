You are a localization engineer tasked with updating the company's translation repositories. You have received several translation updates in wide-format CSVs from external translators, and you need to merge them into our existing long-format localization files.

Here is your task:
1. You will find multiple CSV files in `/home/user/locales/updates/`. Each CSV is in a wide format with the header: `string_id,en,es,fr,de`.
2. There is an existing base translations file at `/home/user/locales/base.json`. It is structured as: `{"<locale_code>": {"<string_id>": "<translation>"}}`.
3. Write a Python script at `/home/user/process_locales.py` that:
   - Uses Python's `multiprocessing` or `concurrent.futures` module to read and parse all CSV files in `/home/user/locales/updates/` in parallel.
   - Reshapes the wide-format CSV data into a long-format/nested dictionary structure.
   - Merges the new translations into the data from `base.json`. If a `string_id` already exists in the base JSON for a locale, the CSV value should overwrite it.
   - Writes the fully merged translation data to a new JSON file at `/home/user/locales/output/final.json` (indented with 2 spaces, keys sorted alphabetically).
   - Generates INI-style files for each locale (excluding 'en') in `/home/user/locales/output/`. Name them `final_<locale>.ini` (e.g., `final_es.ini`). Each INI file should have a single section `[translations]` followed by `string_id=translation` pairs, sorted alphabetically by `string_id`.
4. Run your script to generate the output files.

Make sure the directory `/home/user/locales/output/` exists before writing to it.