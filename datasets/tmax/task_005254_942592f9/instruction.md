You are a data analyst tasked with building a robust data sanitization pipeline for incoming customer CSV files. 

We have a strict compliance policy regarding sensitive data, but the exact policy rule was only provided to us as a scanned screenshot of a memo, located at `/app/policy.png`. 

Your task is to:
1. Extract the sensitive data pattern from the image `/app/policy.png`. (You may use tools like `tesseract` which is pre-installed).
2. Create a Rust project in `/home/user/filter_project`.
3. Write a Rust command-line tool within this project that takes a single file path as an argument (the input CSV).
4. The tool must parse the CSV, which has the columns: `transaction_id`, `user_id`, `timestamp`, `comments`.
5. The tool must perform the following transformations:
   - **Deduplication:** Group and sort by `user_id`, keeping only the *first* chronologically occurring record for each `user_id` (based on the `timestamp` column, formatted as ISO8601).
   - **Sanitization / Filtering:** Completely drop any row where the `comments` column matches or contains the sensitive data pattern found in the policy image.
   - **Normalization:** Ensure all text in the `comments` column has leading and trailing whitespace stripped.
6. The tool must print the resulting cleaned CSV data to standard output (`stdout`), including the header row.

Your Rust program will be rigorously evaluated against two hidden datasets: a "clean" corpus of valid transactions, and an "evil" corpus of malicious or sensitive records that must be strictly rejected. 

Ensure your Rust program can be run directly using `cargo run -- <input.csv>` from within the `/home/user/filter_project` directory.