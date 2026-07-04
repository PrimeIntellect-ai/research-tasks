You are managing a configuration tracking system. The system exports change logs to a CSV file, but the export format is messy. Specifically, the `Diff` column contains raw configuration changes that often include embedded newlines. Previous naive shell scripts failed to process these files correctly, dropping or mangling multi-line records.

Your task is to properly parse this CSV, extract specific features from the text, compute user statistics, and load the processed data into an SQLite database. 

**Input File:**
A CSV file is located at `/home/user/config_changes.csv`. 
It has the following columns: `ChangeID`, `Timestamp`, `User`, `Diff`.
*Note: The `Diff` column is quoted and contains embedded newlines.*

**Processing Requirements:**
1. **Robust Parsing:** Read the CSV file correctly, preserving all rows and handling embedded newlines within the `Diff` column.
2. **Feature Extraction:** Use Regular Expressions to extract newly added IPv4 addresses from the `Diff` text. 
   - A newly added IP is identified by a line within the `Diff` text that starts *exactly* with `+ IP: ` followed by a valid IPv4 address.
   - Example: `+ IP: 192.168.1.100` (Extract `192.168.1.100`).
   - A single `Diff` might contain zero, one, or multiple added IPs. Extract all of them.
3. **Aggregation:** Calculate the total number of configuration changes (rows) authored by each `User`.

**Output Requirements:**
Create an SQLite database at `/home/user/tracker.db` and insert your results into two tables with the exact schemas below:

1. **Table:** `user_stats`
   - `User` (TEXT): The username.
   - `ChangeCount` (INTEGER): The total number of changes made by this user.

2. **Table:** `extracted_ips`
   - `ChangeID` (TEXT): The ID of the change.
   - `IP_Address` (TEXT): The extracted IPv4 address.
   *Note: If a change has multiple added IPs, insert a separate row for each. If a change has no added IPs, do not insert any rows for that ChangeID.*

You may write a script in Python, Node.js, or any other language available in the standard environment to accomplish this.