You are a data engineer tasked with building an ETL pipeline in Rust that merges user activity logs with financial transaction records. Both systems record timestamps slightly differently, and you need to align them while ensuring user PII is masked before the data lands in our analytics warehouse.

**Input Datasets:**
1. **Activity Logs**: A JSONL file located at `/home/user/data/logs.jsonl`
   Each line contains: `{"ts": "<ISO8601 timestamp>", "uid": "<user_id>", "ip": "<ip_address>", "email": "<email_address>"}`
2. **Transactions**: A CSV file located at `/home/user/data/tx.csv`
   Columns: `tx_ts,uid,amount`
   (Timestamps are also ISO8601, and amount is a floating-point number).

**Your Task:**
Write and execute a Rust program (using `cargo new` in `/home/user/etl_pipeline`) that reads both files and produces a joined, aggregated, and masked JSONL file at `/home/user/output/merged.jsonl`.

**Processing Rules:**
1. **Timestamp Alignment:** Parse the timestamps from both datasets. Truncate both timestamps to the *minute* (e.g., `2023-10-25T14:32:45Z` becomes `2023-10-25T14:32:00Z`). 
2. **Join & Aggregate:** Join the logs and transactions on `uid` AND the *minute-truncated timestamp*. 
   - If a user has multiple transactions in the same minute, sum their `amount`s.
   - Only output records that exist in *both* the logs and the transactions datasets for that minute (Inner Join).
3. **Data Masking:**
   - **IP Address:** Replace the last octet of the IPv4 address with `0` (e.g., `192.168.1.50` -> `192.168.1.0`).
   - **Email:** Mask the local part of the email (before the `@`) by keeping only the first letter and replacing the rest of the local part with `***`. (e.g., `john.doe@gmail.com` -> `j***@gmail.com`).

**Output Format:**
Create `/home/user/output/merged.jsonl`. Each line must be a JSON object with the following exact keys:
`minute` (String, the truncated ISO8601 timestamp ending in `00Z`), `uid` (String), `masked_ip` (String), `masked_email` (String), `total_amount` (Float, rounded to 2 decimal places).

Ensure your Rust code compiles and runs successfully, generating the required output file. You may use any standard crates (like `serde`, `serde_json`, `csv`, `chrono`) by adding them to your `Cargo.toml`.