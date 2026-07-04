You are a data analyst tasked with processing a batch of sensitive event logs. The raw data is messy, contains Personally Identifiable Information (PII), and uses inconsistent timestamp formats.

Your objective is to write a single Bash script at `/home/user/process_events.sh` that automates the extraction, transformation, and loading (ETL) of this data, and generates a summary report.

Here are your exact requirements:

1. **Input Data**: A raw CSV file is located at `/home/user/raw_events.csv` (header: `id,timestamp,email,action,amount`).
2. **Data Masking (Anonymization)**:
   - Read the CSV and mask the `email` column. 
   - Replace the username portion (everything before the `@` symbol) with exactly `***`. For example, `john.doe@example.com` must become `***@example.com`.
3. **Timestamp Alignment**:
   - The `timestamp` column contains a mix of Unix epoch timestamps (e.g., `1672531200`) and ISO8601 strings (e.g., `2023-01-01T01:30:00Z`).
   - Convert all timestamps to a uniform UTC format: `YYYY-MM-DD HH:MM:SS`.
4. **Database Bulk Import**:
   - Create a SQLite database at `/home/user/analytics.db`.
   - Create a table named `events` with the schema: `id INTEGER, timestamp TEXT, email TEXT, action TEXT, amount INTEGER`.
   - Import your cleaned and masked CSV data into this table.
5. **Template-Based Generation**:
   - An HTML template is located at `/home/user/template.html`.
   - Query your SQLite database to calculate three metrics:
     - `{{TOTAL_EVENTS}}`: The total number of rows.
     - `{{UNIQUE_DOMAINS}}`: The count of unique email domains (since the username is masked, just count unique masked emails).
     - `{{TOTAL_AMOUNT}}`: The sum of the `amount` column.
   - Replace the placeholders in `template.html` with these exact computed values.
   - Save the final generated HTML file to `/home/user/report.html`.

Constraints:
- You must use Bash (`/home/user/process_events.sh`) to perform all operations.
- The script must be executable.
- Do not leave any intermediate unmasked CSV files on disk after the script finishes.

Run your script to ensure all files (`/home/user/analytics.db` and `/home/user/report.html`) are created properly.