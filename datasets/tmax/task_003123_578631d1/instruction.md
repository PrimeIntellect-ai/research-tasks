You are an AI assistant acting as a localization engineer. You need to consolidate translation files from different platforms into a single unified format. 

Currently, our translations are scattered across two files in `/home/user/locales/`:
1. `app_strings.json`: Contains mobile app translations in a "long" format. 
   Structure: `[{"key": "string_id", "language": "lang_code", "translation": "value"}, ...]`
2. `web_strings.csv`: Contains web app translations in a "wide" format. 
   Structure: `key,en,es,fr,de` where columns are language codes and values are the translations.

Your task is to write and execute a Python script that performs the following data processing pipeline:

1. **Environment Setup:** Install any necessary Python libraries (e.g., `pandas`, `pyarrow`) into your environment.
2. **Read and Reshape:** 
   - Load both files. 
   - Reshape `web_strings.csv` from wide to long format so it has three columns: `key`, `language`, and `translation`. Drop any rows where the translation is missing/null.
3. **Hash-Based Deduplication:** 
   - Combine both datasets. 
   - Create a new column named `hash_id` which contains the SHA256 hash of the string `<key>_<language>` (e.g., if key is "login" and language is "en", the hash input is "login_en").
   - Deduplicate the dataset based on `hash_id`. We have overlapping keys between mobile and web. **Priority rule:** If a `hash_id` appears in both datasets, you MUST keep the translation from `app_strings.json` and discard the one from `web_strings.csv`.
4. **Export:** 
   - Ensure the final dataset has exactly these columns: `hash_id`, `key`, `language`, `translation`.
   - Sort the dataset alphabetically by `key`, then by `language`.
   - Save the final dataset to two formats in the directory `/home/user/locales_processed/`:
     a) A CSV file named `unified_translations.csv` (comma-separated, include headers, no index).
     b) A Parquet file named `unified_translations.parquet`.

Make sure to create the output directory `/home/user/locales_processed/` before saving the files. Complete the task using a Python script.