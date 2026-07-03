You are acting as a localization engineer. We are preparing a new release and need to update our Spanish translation files. 

Our application's master English keys are stored in `/home/user/base_en.json`. 
Our translation agency has uploaded the latest Spanish translations to a remote staging directory mounted at `/tmp/remote_loc/es_updates.csv`.

Your task is to write and execute a Python script to perform the following:
1. **Fetch** the `es_updates.csv` file from `/tmp/remote_loc/` to your working directory `/home/user/`.
2. **Read and Merge** the translations. You must create a complete translation mapping for every key present in `base_en.json`. 
   - If a key from `base_en.json` exists in `es_updates.csv`, use the Spanish translation.
   - If a key from `base_en.json` is missing from the CSV, fallback to the English string from `base_en.json`.
   - Ignore any keys in the CSV that do not exist in `base_en.json`.
3. **Normalize Placeholders**: The agency often messes up our placeholder syntax. In both the Spanish translations and the English fallbacks, you must find any placeholder formatted with brackets (e.g., `[ User ]`, `[APP_NAME]`, `[  item_count  ]`) and normalize it to our system's standard curly brace format, lowercased, with no surrounding spaces (e.g., `{user}`, `{app_name}`, `{item_count}`). 
   - Rule: Replace `[` followed by any amount of whitespace, then a variable name (alphanumeric and underscores), followed by any amount of whitespace, then `]` with `{lowercase_variable_name}`.
4. **Output**: Save the final merged and normalized translations to `/home/user/es_final.json`. The JSON must be pretty-printed with an indent of 4 spaces, keys sorted alphabetically.

Example placeholder normalization:
"Hola [ Name ], bienvenido a [ APP_NAME ]!" -> "Hola {name}, bienvenido a {app_name}!"

Please write and run the Python script to generate `/home/user/es_final.json`.