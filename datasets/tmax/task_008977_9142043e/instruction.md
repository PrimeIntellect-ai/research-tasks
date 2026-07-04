You are a localization engineer managing translations for a software project. You need to build a C++ data processing pipeline to merge translation files, calculate coverage statistics, and prepare a shell script and cron configuration for automated daily processing.

The translation files are provided as simple CSV files (comma-separated, without quotes, no commas inside text) in `/home/user/translations/`. 
The files are: `en.csv` (base language), `fr.csv`, `ja.csv`, and `es.csv`. The first row is the header: `key,text`.

Your task:
1. Write a C++ program at `/home/user/process_translations.cpp`. When compiled and executed, it should:
   - Read the keys from `en.csv` as the master list. All keys in `en.csv` must appear in the final output.
   - Read `fr.csv`, `ja.csv`, and `es.csv` to merge the translations.
   - Output a Tab-Separated Values (TSV) file to `/home/user/translations/merged.tsv` with the header exactly as: `key	en	fr	ja	es`. If a translation is missing for a key, leave that column blank. The rows should be in the same order as the keys appear in `en.csv`.
   - Calculate summary statistics for each language (including `en`). The statistics required are:
     a) Translation coverage percentage (integer division: `(translated_keys * 100) / total_master_keys`).
     b) Total number of Unicode characters (code points) across all translated text for that language. Note: Count characters, not bytes. The text is UTF-8 encoded.
   - Write these statistics to `/home/user/translations/stats.txt` with exactly this format for each language (in the order en, fr, ja, es):
     `[lang]: [coverage]%, [total_chars]`
     Example line: `fr: 66%, 16`

2. Write a bash script `/home/user/run_pipeline.sh` that compiles `/home/user/process_translations.cpp` (outputting the executable to `/home/user/process_translations`) and runs it. Make sure the script has execution permissions.

3. Write a crontab entry to a file `/home/user/cron_schedule.txt` that schedules `/home/user/run_pipeline.sh` to run at exactly 2:30 AM every Sunday.

Compile and run your pipeline once to ensure `merged.tsv` and `stats.txt` are generated successfully.