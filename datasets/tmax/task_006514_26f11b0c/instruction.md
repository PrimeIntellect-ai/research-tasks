You are an AI assistant helping a data scientist set up a daily automated data cleaning pipeline. The scientist receives a daily dump of patient records that are poorly formatted, improperly encoded, and contain sensitive Personally Identifiable Information (PII) and missing values. The file can be very large (up to several gigabytes), so it must be processed efficiently.

Your task is to write a Python script that cleans this data and then schedule it using cron.

**Requirements:**

1. **Python Script (`/home/user/clean_pipeline.py`):**
   Write a Python script that reads from `/home/user/data/incoming.csv` and writes the cleaned data to `/home/user/data/processed.csv`.
   * **Large-file streaming:** You must process the file line-by-line or in chunks (e.g., using Python's `csv` module or pandas with `chunksize`) so that it does not load the entire file into memory at once.
   * **Character encoding handling:** The input file is encoded in `cp1252` (Windows-1252). The output file must be saved in `utf-8`.
   * **Data masking and anonymization:**
     * The `email` column must be replaced with its SHA-256 hash (hexadecimal digest).
     * The `ssn` column contains Social Security Numbers in the format `XXX-XX-XXXX`. You must mask the first 5 digits with asterisks, keeping the hyphens intact. For example, `123-45-6789` becomes `***-**-6789`.
   * **Interpolation and imputation:**
     * The `temperature` column contains patient body temperatures (floats). Some rows have missing values (represented as empty strings). You must impute these missing values with the fixed float `98.6`. Keep existing values as they are.
   * Do not alter the `id`, `name`, or `notes` columns. Keep the original header row in the output.

2. **Pipeline Scheduling:**
   Create a cron job for the `user` account that executes this Python script exactly at **03:15 AM** every day. The cron job should run `python3 /home/user/clean_pipeline.py`.

3. **Execution:**
   After writing the script and configuring the cron job, manually run your script once so that `/home/user/data/processed.csv` is generated and available for verification.

Ensure that all file paths are exactly as specified.