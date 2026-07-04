You are tasked with building a bash script to process and ingest configuration management tracking data. 

A configuration management system exports server status snapshots as CSV files into the `/home/user/cmdb_exports/` directory. However, the system is legacy and inconsistent:
1. The CSV files are in a "wide" format: `Timestamp,Server1,Server2,Server3`.
2. The `Timestamp` includes full date and time (e.g., `2023-10-01T10:00:00Z`).
3. Some of the CSV files are encoded in `ISO-8859-1` while others are in `UTF-8`. The status values often contain French accented characters (e.g., `Dégradé`).

Write a Bash script at `/home/user/process_config.sh` that performs the following multi-stage pipeline:
1. **Character Encoding:** Reads all `.csv` files in `/home/user/cmdb_exports/` and ensures all data is properly handled and converted to standard `UTF-8`.
2. **Reshaping:** Converts the wide-format CSV into a long format without headers. For a row like `2023-10-01T10:00:00Z,Actif,Inactif,Dégradé`, it should produce three separate records (one for each server).
3. **Time-based Bucketing:** Extracts only the `YYYY-MM-DD` date from the Timestamp. Discard the time portion.
4. **Database Import:** Creates a SQLite database at `/home/user/cmdb_tracking.db` and bulk imports the long-format records into a table named `daily_status`.

**Table Schema:**
The SQLite table must be created with this exact schema:
`CREATE TABLE daily_status (date TEXT, server TEXT, status TEXT);`

**Requirements:**
- Do not insert the header rows into the database.
- Keep the server names exactly as they appear in the CSV header (e.g., `Server1`, `Server2`, `Server3`).
- The script must be self-contained and idempotent (if you run it on a fresh system, it creates the DB and inserts the records).
- Use standard bash tools (`awk`, `sed`, `iconv`, `sqlite3`, etc.).

Execute your script so the database is populated and ready for verification.