You are a localization engineer managing a continuous translation pipeline. External translators submit translations which are collected into a raw CSV file. Currently, the legacy scripts silently drop rows or break because translation strings often contain embedded newlines. 

Your task is to build a reliable Rust-based processing step that handles these newlines correctly, anonymizes the data, aggregates it into time buckets, and generates a stratified sample for QA.

**Setup Requirements:**
A raw data file is located at `/home/user/raw_translations.csv`. It has the following columns:
`timestamp,translator_id,locale,translation_text`

The `translation_text` fields are enclosed in double quotes and may contain literal embedded newline characters. 

**Task:**
1. Create a Rust project at `/home/user/loc_pipeline`. You may use the `csv` and `serde` crates.
2. Write a Rust program that reads `/home/user/raw_translations.csv` and correctly parses the quoted fields with newlines.
3. **Time-based bucketing:** Parse the `timestamp` (format: `YYYY-MM-DDTHH:MM:SSZ`) and bucket the records by hour. The bucket format should be `YYYY-MM-DD-HH`.
4. **Data masking:** Replace the `translator_id` with the string `"MASKED"`.
5. **Data sampling and stratification:** For each unique combination of `bucket` and `locale`, select up to the **first 2** translations submitted (sorted chronologically by the original timestamp). Discard the rest.
6. **Transformation:** In the `translation_text`, replace any embedded newline characters (`\n` or `\r\n`) with the literal string `\n` (a backslash followed by the letter n) so the output is strictly one line per record.
7. Write the processed results to `/home/user/processed_samples.csv` with the following headers:
`bucket,locale,masked_id,cleaned_text`
Ensure the output rows are sorted alphabetically by `bucket`, then by `locale`, then by the original `timestamp` ascending.
8. Create a bash script at `/home/user/run_pipeline.sh` that compiles (if necessary) and runs your Rust program. Ensure it has execute permissions.

Run your pipeline script so that `/home/user/processed_samples.csv` is created.