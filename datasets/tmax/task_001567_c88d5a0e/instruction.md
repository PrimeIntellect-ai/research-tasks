You are a Database Reliability Engineer investigating a suspect database backup. 

During a recent restore drill, a backup artifact `/home/user/db_backup.sqlite` was recovered, but the automated logs indicate that foreign key constraints were temporarily disabled during the initial backup creation, potentially leading to referential integrity violations (orphaned records). 

Your task is to write a Bash script at `/home/user/analyze_backup.sh` that analyzes the SQLite backup, identifies referential integrity violations, aggregates the financial impact of these corrupted records, and outputs a strict JSON report.

The database contains at least three tables: `customers`, `orders`, and `payments`. The schema uses standard foreign keys (e.g., `orders.customer_id` references `customers.id`, and `payments.order_id` references `orders.id`). Both `orders` and `payments` tables have an `amount` column (numeric).

Your Bash script must perform the following:
1. Use the `sqlite3` CLI to programmatically detect foreign key violations (orphaned records) across the entire database.
2. Cross-reference the identified orphaned records to calculate:
   - The total count of orphaned `orders`.
   - The sum of the `amount` column for all orphaned `orders`.
   - The total count of orphaned `payments`.
   - The sum of the `amount` column for all orphaned `payments`.
3. Generate a validated JSON report at `/home/user/integrity_report.json` with exactly the following schema:
```json
{
  "orphaned_orders_count": <integer>,
  "orphaned_orders_amount": <float, 2 decimal places>,
  "orphaned_payments_count": <integer>,
  "orphaned_payments_amount": <float, 2 decimal places>
}
```

Rules:
- You must write the logic in pure Bash, using `sqlite3`, `jq`, `awk`, or standard GNU coreutils. Do not use Python, Ruby, or other scripting languages.
- Ensure the output JSON is strictly formatted and valid. Amounts should be formatted to exactly 2 decimal places (e.g., `150.00`, not `150.0` or `150`). If an amount is 0, it should be `0.00`.
- Your script must be executable (`chmod +x /home/user/analyze_backup.sh`) and produce the report when run. Run your script to generate the final `integrity_report.json` file.