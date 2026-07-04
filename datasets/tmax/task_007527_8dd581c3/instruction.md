You are a data engineer building an ETL pipeline. We have a daily batch of user feedback data in a CSV file that needs cleaning, anonymization, and validation before being loaded into our data warehouse. 

There is an initialized Rust Cargo project located at `/home/user/etl_pipeline`. The input data is located at `/home/user/etl_pipeline/input.csv`.

Your task is to write a Rust program in `/home/user/etl_pipeline/src/main.rs` that reads `input.csv`, processes the data according to the rules below, and writes the results to `/home/user/etl_pipeline/output.csv`.

Processing Rules:
1. **Parsing**: The CSV contains four columns: `id`, `email`, `score`, and `comments`. You must properly parse the CSV. Be careful: the `comments` column sometimes contains embedded newlines, which must be preserved intact without breaking the row parsing.
2. **Validation Gate (Constraints)**: You must drop any rows where the `score` is missing (empty), not a valid integer, or less than 0. Only keep rows with `score >= 0`.
3. **Data Masking (Anonymization)**: For the `email` column, you must mask the local part of the email address (everything before the `@` symbol) by replacing it completely with three asterisks (`***`). For example, `john.doe_89@company.com` should become `***@company.com`. If an email does not contain an `@`, replace the entire string with `***`.
4. **Output**: Write the valid, masked rows to `output.csv` in the exact same format and column order (`id,email,score,comments`). Include the header row. Standard CSV quoting rules should apply to the output (e.g., fields with newlines must be quoted).

The `Cargo.toml` has already been configured with the `csv` and `serde` (with `derive` feature) crates. Write the code, compile, and run the pipeline to generate `output.csv`.