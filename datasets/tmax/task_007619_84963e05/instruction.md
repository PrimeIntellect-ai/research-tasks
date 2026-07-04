You are acting as a log analyst investigating patterns in a multi-language server environment. You have been provided with an export of application logs in JSON format, containing error messages in multiple languages (English, Russian, Japanese). 

Your task is to write a Rust tool to process these logs, extract specific features, normalize the unicode text, and bulk import the results into a database for analysis.

Here are the specific requirements:
1. The input file is located at `/home/user/logs.json`. It contains a JSON array of log objects. Each object has the following schema:
   - `ts` (integer): Unix timestamp
   - `code` (integer): HTTP error code
   - `msg` (string): Error message in various languages
   - `host` (string): Originating server

2. Create a Rust project named `log_processor` in `/home/user/`.
3. Write a Rust program in this project that reads `/home/user/logs.json` and performs the following data transformations:
   - Extracts only the `ts`, `code`, and `msg` fields.
   - Normalizes the `msg` field by converting the entire unicode string to lowercase.
4. The Rust program must write the transformed data to a CSV file at `/home/user/processed_logs.csv` with the exact headers: `timestamp,error_code,message`.
5. Once the CSV is generated, use the SQLite command-line tool (`sqlite3`) to bulk import `/home/user/processed_logs.csv` into an SQLite database located at `/home/user/analysis.db`.
   - The table must be named `normalized_logs`.
   - Ensure the database schema for the table matches the CSV columns.

Please compile and run your Rust program, and execute the SQLite import. Do not use any external services; everything must be done locally.