You are a localization engineer tasked with cleaning and processing a raw dump of translation strings. The raw data is located at `/home/user/translations.jsonl`. 

You need to write a Rust program in `/home/user/i18n_processor` to process this data. 

The input file `/home/user/translations.jsonl` contains one JSON object per line with the following structure:
`{"locale": "...", "key": "...", "text": "...", "features": null}`
Note: The `text` field might be `null` or an empty string `""` for some non-English locales.

Your Rust program must perform the following pipeline:
1. **Imputation**: If the `text` field for a key in a non-`en-US` locale is missing (`null` or `""`), you must impute it by falling back to the `en-US` text for that exact same `key`. You can assume `en-US` contains a valid, non-empty string for every key.
2. **Feature Extraction**: Replace the `features` null value with an object containing two metrics about the final (imputed or original) `text`:
   - `char_count`: The number of Unicode scalar values in the string (e.g., "A" is 1, an emoji like "👋" is 1).
   - `placeholders`: The integer count of localization placeholders in the string. A placeholder is strictly defined as any text enclosed in `{` and `}`, with no nested braces (e.g., `{username}` counts as 1, `{user_{id}}` is invalid and you only need to match standard `{xyz}` patterns).
3. **Grouping and Sorting**: Group the records by their `locale`. Within each locale group, sort the records alphabetically by their `key`.
4. **Output**: Write the final processed data to `/home/user/processed_translations.json`. The output must be a single JSON object where the keys are the `locale` strings, and the values are arrays of the processed JSON objects (containing `locale`, `key`, `text`, and the new `features` object). The JSON should be pretty-printed with 2 spaces.

Initialize the Rust project yourself. You may use external crates like `serde`, `serde_json`, and `regex`. 
Run your program so that `/home/user/processed_translations.json` is generated correctly.