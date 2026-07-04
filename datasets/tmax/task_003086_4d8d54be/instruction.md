You are a data analyst tasked with cleaning an international weather sensor dataset. The raw data is located at `/home/user/sensors_raw.csv`.

The CSV has three columns: `date` (YYYY-MM-DD), `station` (string), and `temp` (float, but some are missing). 

The dataset has several issues that you need to fix using a Python script:
1. **Unicode Inconsistency:** The `station` names contain international characters, but they are mixed between NFC and NFD Unicode normalization forms (e.g., "München" might be represented differently). You must normalize all `station` strings to **NFC**.
2. **Duplicates:** After normalizing the station names, there are duplicate rows in the dataset. You must remove exact duplicate rows (keep the first occurrence).
3. **Missing Data:** Some `temp` values are missing (empty strings). For each `station`, sort the records chronologically by `date` and fill the missing `temp` values using linear interpolation. (Assume the first and last dates for each station are never missing).
4. **Format Conversion:** Save the cleaned, interpolated dataset as a JSON Lines file at `/home/user/sensors_clean.jsonl`. Each line should be a JSON object with keys `date`, `station`, and `temp`. The output must be sorted by `station` (alphabetically) and then by `date`.
5. **Logging:** Create a log file at `/home/user/processing.log`. Your script must write exactly two lines to this log file (in this order):
   - `Duplicates removed: X` (where X is the number of rows dropped)
   - `Imputed values: Y` (where Y is the number of missing `temp` values that were interpolated)

Use Python (e.g., `pandas`) to perform these operations.