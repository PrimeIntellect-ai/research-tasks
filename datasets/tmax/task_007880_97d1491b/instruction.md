You are a log analyst investigating suspicious access patterns in our internal systems. We need a Rust tool to analyze logs, correlate them with personnel records, and output anonymized reports of suspicious activity.

You have been provided with two files:
1. `/home/user/access_logs.csv`
   Columns: `timestamp,ip_address,emp_id,status_code,endpoint`
   Contains web server access logs.

2. `/home/user/employees.csv`
   Columns: `emp_id,full_name,email,department`
   Contains employee metadata.

Your task is to write and execute a Rust program that does the following:
1. **Anomaly Detection**: Parse `/home/user/access_logs.csv` and identify employees who have experienced a sudden "denial spike" — defined as strictly more than 3 `403` (Unauthorized) status codes.
2. **Join**: Correlate these flagged `emp_id`s with the records in `/home/user/employees.csv` to retrieve their email addresses.
3. **Data Masking**: Anonymize the email addresses of the flagged employees to protect PII. The masking rule is:
   - Keep the first letter of the local part (before the `@`).
   - Replace the remaining characters of the local part with asterisks (`*`), preserving the exact length.
   - Keep the domain part intact.
   - Example: `alice.smith@corp.com` becomes `a**********@corp.com` (1 letter, 10 asterisks).
4. **Output**: Generate a CSV file at `/home/user/suspects.csv` with the header `emp_id,masked_email,error_count`. Include one row for each flagged employee, sorted in ascending order by `emp_id`.

Constraints:
- You must use **Rust** to process the data. You can initialize a new cargo project in `/home/user/log_analyzer` or write a single file.
- Do not modify the original CSV files.