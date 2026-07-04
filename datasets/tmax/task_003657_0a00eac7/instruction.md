You are a data engineer modernizing an ETL pipeline. Incoming data batches are CSV files containing hierarchical financial account structures with the following header:
`account_id,parent_account_id,balance,account_type`

Previously, a proprietary compiled C program located at `/app/legacy_validator` was used to validate these CSVs. It is a stripped binary that returns exit code 0 for valid files and 1 for invalid files. We need to replace it with a transparent, maintainable Bash script that uses SQLite3.

Your task is to write a Bash script at `/home/user/etl_filter.sh` that takes a single argument (the path to a CSV file), loads it into an SQLite database (e.g., in-memory or a temporary file), creates appropriate indexes for performance, and uses complex SQL (including recursive CTEs) to validate the data.

The data is considered valid ONLY if it satisfies ALL the following rules:
1. **No Circular References**: The `account_id` to `parent_account_id` hierarchy must be a directed acyclic graph (no loops).
2. **Maximum Depth**: The maximum depth of the hierarchy (from a root node where `parent_account_id` is empty to any leaf) must not exceed 7. (A root node is depth 1).
3. **Summary Balances**: The `balance` of any account with `account_type` equal to 'Summary' must exactly equal the sum of the `balance`s of its immediate child accounts.
4. **Leaf Constraints**: No account with `account_type` equal to 'Leaf' is allowed to be the `parent_account_id` of any other account.

Your script must exit with code 0 if the CSV is completely valid, and exit with code 1 if it violates any of the rules. 

You can use `/app/legacy_validator` as an oracle to test your logic if you generate your own test CSVs. 
Ensure your script handles potentially large files efficiently by using proper index strategies before executing the hierarchical queries. Make the script executable (`chmod +x`).