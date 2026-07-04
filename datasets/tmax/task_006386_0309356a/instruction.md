You are a localization engineer tasked with updating translation files for a legacy application. The system recently exported a raw log of updated localization strings, but the output is messy, unstructured, and contains un-decoded Unicode escape sequences.

Your task is to write a Rust program that processes this file, standardizes the translations, and outputs them into a clean JSON format.

**Input File:** `/home/user/loc_raw.txt`
The file contains lines with mixed log data. The lines you care about follow this exact pattern:
`[TIMESTAMP] {LANG_CODE} <KEY_NAME> : "VALUE"`

Example line:
`[2023-10-14 10:22:11] {fr-FR} <BTN_SUBMIT> : "Soumettre\u0020!"`

**Requirements:**
1. Create a Rust project or script in `/home/user/loc_processor/`. You may use standard crates (like `regex`, `serde`, `serde_json`).
2. **Regex Pattern Construction:** Use regular expressions to find all matching lines in `/home/user/loc_raw.txt` and extract the `LANG_CODE`, `KEY_NAME`, and `VALUE`. Ignore any line that does not match this pattern.
3. **Character Encoding Handling:** The extracted `VALUE` strings contain Unicode escape sequences (e.g., `\u00E9` for `é`, `\u0020` for space, `\u00F3` for `ó`). You must decode these sequences into their actual UTF-8 characters.
4. **Large-scale Sorting and Grouping:** 
   - Group the translations by `LANG_CODE`.
   - Within each language group, sort the translation entries alphabetically by `KEY_NAME`.
5. **Output:** Write the processed data to `/home/user/loc_clean.json`. The output must be pretty-printed JSON (using 2 spaces for indentation) with the following structure:

```json
{
  "de-DE": {
    "FAREWELL": "Auf Wiedersehen",
    "GREETING": "Hallo Welt"
  },
  "es-ES": {
    "FAREWELL": "Adiós",
    "GREETING": "Hola Mundo"
  }
}
```

Compile and run your Rust program to generate the final `/home/user/loc_clean.json` file.