You are a localization engineer fixing a messy dataset. An ETL job that pulls translations from our translation management system failed and retried, resulting in duplicate records. Additionally, some records were corrupted during extraction and contain Unicode Replacement Characters. 

Your task is to write a Rust program that cleans this data.

I have already set up a Rust project for you at `/home/user/l10n_processor` with `serde`, `serde_json`, and `csv` added as dependencies.

The input data is located at `/home/user/l10n_processor/input.json`. It contains a JSON array of objects, each with the following schema:
- `key` (string): The translation key (e.g., "ui.button.submit")
- `lang` (string): The language code (e.g., "en", "ja", "es")
- `text` (string): The translated text
- `timestamp` (integer): The Unix timestamp of when the translation was extracted

Write a Rust program in `/home/user/l10n_processor/src/main.rs` that does the following:
1. Reads the `input.json` file.
2. Filters out any records where the `text` is empty OR contains the Unicode Replacement Character (``, U+FFFD).
3. Resolves duplicates caused by the ETL retry: If there are multiple records with the same `key` and `lang`, keep ONLY the record with the highest `timestamp`.
4. Writes the cleaned and deduplicated records to `/home/user/l10n_processor/output.csv`.
5. The output CSV must have the headers `key,lang,text` and must be sorted alphabetically ascending first by `key`, and then by `lang`.

Once your Rust program is written, run it using `cargo run` inside the project directory to generate the `output.csv` file.