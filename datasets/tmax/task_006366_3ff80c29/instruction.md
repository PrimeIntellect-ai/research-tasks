You are a data engineer responsible for building an ETL pipeline to process legacy application logs using Bash. 

You have been provided with a raw log file located at `/home/user/raw_logs.txt`. 
The file contains unstructured and malformed data. Your task is to extract valid records, normalize them, and bulk load them into an SQLite database.

**Step 1: Data Validation and Filtering**
A valid log line strictly follows this format:
`[YYYY/MM/DD] [LEVEL] <UserID> - Message`

You must filter the file to keep ONLY lines that meet ALL of the following constraints:
1. The Date must be enclosed in square brackets `[]` and formatted exactly as `YYYY/MM/DD` (where Y, M, D are digits).
2. The Level must be enclosed in square brackets `[]` and be exactly one of: `INFO`, `WARN`, or `ERROR`.
3. The UserID must be enclosed in angle brackets `<>` and consist of exactly 8 alphanumeric characters (uppercase, lowercase, or digits).
4. There must be a literal ` - ` (space, hyphen, space) separating the UserID and the Message.
5. The Message consists of any remaining characters on the line.

**Step 2: Tokenization and Normalization**
For all valid lines, you must transform the data:
1. Normalize the Date format to `YYYY-MM-DD` (replace slashes with hyphens).
2. Strip the enclosing brackets `[]` and `<>` from the Date, Level, and UserID.
3. Convert the entire Message string to lowercase.
4. Format the output as a strict comma-separated values (CSV) string in this column order: `date,level,user_id,message`.

*Example transformation:*
Valid raw line: `[2023/10/05] [INFO] <A1B2c3D4> - SYSTEM booted up`
Normalized CSV line: `2023-10-05,INFO,A1B2c3D4,system booted up`

**Step 3: Database Bulk Import**
1. Create a new SQLite database at `/home/user/processed_logs.db`.
2. Inside this database, create a table named `normalized_logs` with the following schema:
   `CREATE TABLE normalized_logs (date TEXT, level TEXT, user_id TEXT, message TEXT);`
3. Bulk import your normalized CSV data into the `normalized_logs` table.

You must complete this entire pipeline using only Bash built-in tools (like `grep`, `sed`, `awk`) and the `sqlite3` command-line utility. Do not write Python, Perl, or Ruby scripts.