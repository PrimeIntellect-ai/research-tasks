You are a log analyst investigating access patterns from a legacy mainframe. You have been provided with a raw log file at `/home/user/legacy_audit.log`. 

The legacy system exports logs in a wide format and encodes them in UTF-16LE. Your task is to process this file, extract the relevant data, reshape it, and analyze it using a database.

**Phase 1: Data Processing with C**
Write a C program at `/home/user/parser.c` that does the following:
1. Opens and reads `/home/user/legacy_audit.log` (which is encoded in UTF-16LE).
2. Converts the text to UTF-8. You must use the `iconv` library (available via `<iconv.h>`) for character encoding conversion.
3. Parses each line. The log lines have the following wide-format structure:
   `[YYYY-MM-DD HH:MM:SS] USERNAME :: ACTION -> RESOURCE_1;RESOURCE_2;...;RESOURCE_N`
4. Reshapes this wide format into a long format. For every resource accessed in a single log entry, create a separate record.
5. Writes the normalized, UTF-8 encoded records to a CSV file at `/home/user/parsed_logs.csv` with the exact following header on the first line:
   `timestamp,username,action,resource`
   (Do not include the brackets around the timestamp in the CSV).

**Phase 2: Database Aggregation**
After generating `/home/user/parsed_logs.csv`, use `sqlite3` (which is already installed on the system) to:
1. Create a new SQLite database at `/home/user/audit.db`.
2. Bulk import the CSV into a table named `logs`.
3. Execute a query to find the top 3 resources that were accessed with the action "WRITE", ordered by the number of times they were written to in descending order. If there is a tie, order alphabetically by resource name.
4. Export the results of this query to `/home/user/top_writes.csv` in CSV format (no header row needed for this final output, just `resource,count`).

**Constraints:**
- You must write the parser in C and compile it to `/home/user/parser` using `gcc`.
- Do not use Python or other scripting languages for Phase 1. Shell commands are allowed for compiling, running, and the database operations.