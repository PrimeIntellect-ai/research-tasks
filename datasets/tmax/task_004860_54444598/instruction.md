You are a data analyst tasked with cleaning a large dataset of customer reviews. The raw data is located at `/home/user/input.csv` and contains three columns: `id`, `date`, and `text`. 

Due to a bug in the upstream extraction system, the `text` column contains literal Unicode escape sequences (e.g., `\u2026` instead of `…`, or `\u00e9` instead of `é`). Furthermore, the dataset contains malformed rows that do not have exactly three columns.

Your task is to write and execute a Python script (`/home/user/clean_data.py`) that processes this file with the following strict requirements:

1. **Large-File Streaming**: You must read `/home/user/input.csv` sequentially in a streaming fashion (e.g., line-by-line or chunk-by-chunk) so that the entire file is never loaded into memory at once.
2. **Parallel Data Processing**: You must process the lines in parallel using Python's `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` modules to speed up the text decoding.
3. **Character Encoding Handling**: In the `text` column, find and decode all literal Unicode escape sequences (like `\uXXXX`) into their proper UTF-8 characters. 
4. **Data Validation & Pipeline Logging**: 
   - If a row does not have exactly three columns (after basic CSV parsing), it must be dropped.
   - The `id` of every dropped row must be appended to a log file at `/home/user/dropped.log` (one ID per line). If the row is so malformed it doesn't even have an ID, log `UNKNOWN`.
5. **Output**: Write the successfully processed and cleaned rows to `/home/user/cleaned.csv` as a standard, valid CSV (comma-separated, quoting fields containing commas).
6. **Order Preservation**: The rows in `/home/user/cleaned.csv` MUST preserve the original chronological order of the valid rows from `input.csv`.

Once you have written the script, execute it to generate `/home/user/cleaned.csv` and `/home/user/dropped.log`.

Note: The script should process the data efficiently. Do not rely on external non-standard libraries like `pandas` (which loads everything into memory by default) for the core processing; use built-in Python libraries (`csv`, `multiprocessing`, `re`, `codecs`, etc.).