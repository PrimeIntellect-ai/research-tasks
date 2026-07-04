You are a Data Systems Engineer tasked with repairing and extending a Rust-based data processing pipeline. Your company processes transaction datasets, but the current pipeline has two major issues: it lacks an anomaly detection filter to catch poisoned data, and it suffers from a "data leakage" bug during feature engineering.

You need to create a single Rust command-line tool in `/home/user/pipeline_manager` that handles both anomaly detection and correct feature engineering.

**Step 1: Anomaly Detection (Adversarial Filtering)**
We have been receiving maliciously crafted datasets. The security team has provided an image at `/app/anomaly_rules.png` containing the exact business logic rules that define a "poisoned" record.
1. Extract the text from `/app/anomaly_rules.png` (e.g., using `tesseract`).
2. Implement a `validate` subcommand in your Rust CLI:
   `cargo run --release -- validate <input.csv>`
3. The command must parse the CSV. If *any* row in the CSV matches the poison signature defined in the image, the program must immediately print "REJECT" to standard out and exit with status code `1`.
4. If no rows match the poison signature, the program must print "ACCEPT" and exit with status code `0`.
Your validation logic will be tested against two hidden datasets: a clean corpus and an evil corpus. Your program must reject 100% of the evil files and accept 100% of the clean files.

**Step 2: Fixing Feature Data Leakage**
The pipeline currently normalizes features using Z-score scaling `(value - mean) / std_dev`, but a junior analyst accidentally computed the `mean` and `std_dev` over the *entire* dataset before splitting it into training and testing sets, causing a massive data leak.
1. Implement an `engineer` subcommand in your Rust CLI:
   `cargo run --release -- engineer <input.csv> <output.csv>`
2. The input CSV will have the columns: `transaction_id`, `split_type`, `amount`, and `account_age`. The `split_type` will be either the string `train` or `test`.
3. You must calculate the mean and standard deviation for `amount` and `account_age` strictly using **only the rows where `split_type == 'train'`**.
4. Apply the Z-score normalization `(x - train_mean) / train_std` to *all* rows in the dataset (both `train` and `test` splits) using those training statistics. 
5. Write the fully scaled dataset to the specified `<output.csv>` path, maintaining the original column order and row order, with the scaled values formatted to 4 decimal places.

**Requirements:**
- Build your tool as a standard Rust binary project in `/home/user/pipeline_manager`.
- The CSV parser should safely handle standard formatting (you may use the `csv` and `serde` crates).
- Ensure your binary compiles successfully in release mode.