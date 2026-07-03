You are a localization engineer tasked with automating the processing of translation strings from our external translation vendor. 

Every night, a system dumps raw, unsorted translation strings into a single file at `/home/user/raw_data/translations.tsv`. This file is UTF-8 encoded and has three tab-separated columns: `Key`, `LanguageCode`, and `TranslatedText`.

Your task is to:
1. Write a script at `/home/user/update_translations.py` (you can use Python or Bash) that reads `/home/user/raw_data/translations.tsv`.
2. The script must group the translations by `LanguageCode`.
3. For each language, it must generate a valid JSON file at `/home/user/locales/<LanguageCode>.json`.
4. The JSON file must be a flat key-value dictionary (e.g., `{"apple": "manzana", "greeting": "hola"}`). 
5. The keys inside each JSON file **must be sorted alphabetically**.
6. Ensure the directory `/home/user/locales/` exists before writing.
7. Run your script once to process the current data.
8. Schedule your script to run automatically every day at 3:15 AM. Install this schedule into the current user's crontab. Ensure the cron command uses the absolute path to your script.

Constraints:
- Do not use any external dependencies outside of standard Python 3 or standard Linux utilities.
- Assume the input file contains valid UTF-8 characters including right-to-left languages (e.g., Arabic) and CJK characters. 

Execute the script to verify it works, leaving the generated JSON files in the `/home/user/locales/` directory.