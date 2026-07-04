You are a data analyst setting up an automated ETL pipeline. We receive a messy daily dump of user data at `/home/user/data/raw_users.csv`. 

You need to write a Rust program that cleans this data, and then schedule it to run automatically. 

A Cargo project skeleton has already been created for you at `/home/user/csv_processor`. It has the `csv` and `regex` crates added to its `Cargo.toml`.

Write the Rust code in `/home/user/csv_processor/src/main.rs` to fulfill these requirements:
1. **Stream** the input file `/home/user/data/raw_users.csv` (do not read the entire file into memory at once). The input CSV has headers: `name,email,notes`.
2. **Normalize** the `email` column: convert it to entirely lowercase and trim any leading/trailing whitespace.
3. **Extract** a 6-digit ID from the `notes` column using a regular expression. The ID in the notes varies in format, but generally looks like `UserID: 123456`, `id: 123456`, or `ID-123456`. Use a case-insensitive regex pattern that captures exactly 6 digits following the letters "id" and some optional non-digit characters (e.g., `(?i)id[^\d]*(\d{6})`).
4. **Deduplicate** records based on the extracted 6-digit ID. Keep only the *first* record encountered for each ID and discard subsequent duplicates. If a row does not contain a valid 6-digit ID in the notes, discard the row entirely.
5. **Write** the cleaned data to `/home/user/data/cleaned_users.csv` with the headers: `extracted_id,name,email`.

After writing the code:
1. Compile the Rust project in release mode.
2. Run the compiled binary manually once so that `/home/user/data/cleaned_users.csv` is generated.
3. Schedule the compiled release binary (`/home/user/csv_processor/target/release/csv_processor`) to run daily at exactly 2:30 AM using the user's `crontab`.

Ensure the final `cleaned_users.csv` output exactly matches the requirements and that your crontab is properly installed.