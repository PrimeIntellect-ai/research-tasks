You are an automation specialist tasked with creating a robust data ingestion workflow. A legacy system has exported customer records into several CSV files, but they suffer from inconsistent character encodings, formatting irregularities, and need to be consolidated into a relational database.

Your task is to write a Bash script located at `/home/user/process_customers.sh` that performs the following pipeline:

1. **Character Encoding Handling**: 
   The directory `/home/user/raw_data/` contains three files:
   - `export_a.csv` (Encoded in ISO-8859-1)
   - `export_b.csv` (Encoded in Windows-1252)
   - `export_c.csv` (Encoded in UTF-8)
   Your script must read these files and convert all of them to standard UTF-8.

2. **Normalization and Standardization**:
   The CSVs have no header. The columns are: `id, full_name, phone_number, join_date`.
   Using Bash tools (like `awk`, `sed`, or similar), normalize the unified data according to these rules:
   - **full_name**: Must be converted to Title Case (e.g., "JOHN DOE" or "john doe" becomes "John Doe").
   - **phone_number**: Strip all non-digit characters (e.g., "(555) 123-4567" becomes "5551234567").
   - **join_date**: The input dates are in the format `MM/DD/YYYY`. Convert them to ISO 8601 format `YYYY-MM-DD`.

3. **Database Bulk Import**:
   Create a SQLite3 database at `/home/user/customers.db`.
   Create a table named `customers` with the following schema:
   `CREATE TABLE customers (id INTEGER PRIMARY KEY, full_name TEXT, phone_number TEXT, join_date TEXT);`
   Bulk load your normalized, UTF-8 data into this table.

4. **Export**:
   Query the SQLite database to extract all customers who joined on or after `2020-01-01`.
   Export the result to a comma-separated file at `/home/user/recent_customers.csv`, sorted by `id` in ascending order. The output CSV must not contain headers and should use a standard comma delimiter.

Ensure your script is executable (`chmod +x /home/user/process_customers.sh`) and run it so that the final `/home/user/recent_customers.csv` and `/home/user/customers.db` are generated.