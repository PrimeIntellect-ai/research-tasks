You are an AI assistant acting as a data scientist. An ETL pipeline recently failed and underwent several retries, resulting in a dirty dataset containing duplicate records, missing values, and corrupted text. 

Your task is to write and execute a Python script (`/home/user/clean_pipeline.py`) that processes `/home/user/raw_data.csv` and produces a clean dataset at `/home/user/clean_data.csv`. You must also generate a log file at `/home/user/pipeline.log`.

Perform the following data cleaning steps in order:

1. **Hash-based Deduplication**: Due to pipeline retries, there are duplicate records. Compute an MD5 hash of the concatenated string of the `id`, `user_name`, and `email` columns (e.g., `str(id) + user_name + email`). Keep only the *first* occurrence of each hash (retaining the original row ordering) and drop the subsequent duplicates.
2. **Character Encoding Handling**: The `user_name` column suffers from a mojibake issue. It originally contained UTF-8 characters, but was incorrectly decoded as Latin-1/Windows-1252 at some point, resulting in garbled text (e.g., `RenÃ©`). Fix the encoding in Python to restore the correct characters (e.g., `René`).
3. **Interpolation**: After deduplication, sort the dataset by the `id` column in ascending order. The `score` column contains some missing (NaN/blank) values. Fill these missing values using linear interpolation.
4. **Feature Extraction**: Create a new column called `email_domain` by extracting the domain part of the `email` column (everything after the `@` symbol).

**Pipeline Logging Requirements:**
Throughout your script, you must write strict log messages to `/home/user/pipeline.log`. The file must contain *exactly* these lines (with X, Y, Z, W replaced by the correct integer values):
```
[INFO] Initial records: X
[INFO] Duplicates removed: Y
[INFO] Missing scores interpolated: Z
[INFO] Final records: W
```
*(Note: "Missing scores interpolated" refers to the number of missing/NaN values that were filled in the score column of the deduplicated dataset).*

Ensure your final dataset (`/home/user/clean_data.csv`) is saved as a standard CSV file with headers, and that all numeric columns are correctly formatted.