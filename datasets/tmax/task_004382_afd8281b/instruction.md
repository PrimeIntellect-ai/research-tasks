You are a Data Engineer building a reliable ETL pipeline to process a messy CSV file containing sensitive user data. 

We have a raw data file located at `/home/user/raw/data.csv`. The CSV has the following columns: `id`, `name`, `email`, `dob`, `ssn`, and `notes`.

The CSV file is messy: it contains duplicate records, malformed fields, and embedded newlines in the `notes` column (which standard line-by-line bash parsing usually trips over).

Your task is to write a Rust program (and create a new Cargo project for it in `/home/user/etl_pipeline`) that reads this CSV file, processes it according to the rules below, and writes the valid records to `/home/user/processed/output.jsonl` in JSON Lines format.

**Data Processing Rules:**
1. **Deduplication:** Deduplicate records based on the `id` column. Keep only the *first* occurrence of each `id` and drop any subsequent rows with the same `id`.
2. **Cleaning (Email):** Normalize the `email` column by converting it to lowercase and stripping any leading or trailing whitespace.
3. **Validation (Email):** After normalization, if the `email` does not contain an `@` symbol, drop the entire row.
4. **Validation (DOB):** The `dob` (Date of Birth) field must strictly match the `YYYY-MM-DD` format (i.e., exactly 4 digits, a hyphen, 2 digits, a hyphen, 2 digits). If it does not match, drop the entire row.
5. **Masking/Anonymization (SSN):** The `ssn` field contains Social Security Numbers in the format `XXX-XX-XXXX`. You must mask the first five digits and output the format `***-**-XXXX` (where `XXXX` are the original last four digits). Assume valid rows always have a 9-digit SSN with hyphens.
6. **Embedded Newlines:** Your parser must correctly handle embedded newlines in the `notes` column without breaking the row into multiple records.

**Output Format:**
Write the valid, processed records to `/home/user/processed/output.jsonl`. Each line must be a valid JSON object representing one record with the keys: `id`, `name`, `email`, `dob`, `ssn`, `notes`. 

Create the necessary directories and the Rust project, add your dependencies (e.g., `csv`, `serde`, `serde_json`), write the code, and execute it so that `/home/user/processed/output.jsonl` is generated with the correct data.