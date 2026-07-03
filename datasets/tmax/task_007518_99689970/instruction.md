You are a localization engineer working on a mathematical modeling software. The translators have returned a messy French translation file (`fr_raw.txt`) containing localized mathematical error messages. 

Your task is to create a robust Bash script at `/home/user/loc/compile_loc.sh` that processes this raw data against the English base file (`en_base.txt`) and generates a clean, finalized translation file at `/home/user/loc/fr_final.txt`.

Both files are located in `/home/user/loc/` and follow the format `KEY=STRING`. Placeholders in the strings are represented by brackets, containing alphanumeric characters and underscores (e.g., `[var_x]`, `[matrix_1]`).

Your script must perform the following pipeline:

1. **Validation & Regex Parsing:** For every entry in `fr_raw.txt`, check if the translation string contains the *exact same number* of bracketed placeholders (`[...]`) as the corresponding English base string in `en_base.txt`. If the counts do not match, or if the key does not exist in `en_base.txt`, discard the raw French entry entirely.
2. **Deduplication:** The raw file contains duplicate lines. You must deduplicate the valid French entries. If there are multiple valid translations for the *same* key, keep only the *first* one that appears in `fr_raw.txt`.
3. **Gap-Filling:** After validation and deduplication, some keys from `en_base.txt` will be missing in the French set (either they were never translated, or the translations were discarded). You must gap-fill these missing keys by falling back to the exact English string from `en_base.txt`.
4. **Sorting:** The final output must contain exactly the same keys as `en_base.txt`. Sort the final key-value pairs in ascending alphanumeric order based on the keys.

Save the final processed output strictly to `/home/user/loc/fr_final.txt`.

Do not hardcode the expected outputs; your script should dynamically process the files. Execute your script to generate the final output.