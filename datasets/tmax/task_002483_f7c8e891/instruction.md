You are acting as a compliance officer performing an urgent security audit on an undocumented access control system. 

An old SQLite database file has been provided to you at `/home/user/access_logs.db`. Unfortunately, there is no documentation, and the original developers did not use standard naming conventions or explicit foreign key constraints. 

Your task is to analyze the database schema, deduce the relationships between the tables, and extract a specific set of suspicious access records.

Specifically, you need to find all instances where an employee from the "Engineering" department successfully badged into any zone with a clearance level of 4 or higher (inclusive) strictly between `2023-10-01 22:00:00` and `2023-10-02 05:00:00` (inclusive). Only consider 'GRANT' actions (ignore 'DENY').

Once you have crafted the correct query, export the results to a CSV file located exactly at `/home/user/compliance_report.csv`. 

The CSV file must meet the following strict requirements:
1. It must contain exactly three columns with the following headers (in this exact order): `EmployeeName,ZoneName,SwipeTime`
2. It must be comma-separated.
3. The records must be sorted chronologically by the swipe time (oldest first).
4. Do not include any quotes around the fields unless required by standard CSV escaping rules.

Use standard shell tools and `sqlite3` to accomplish this.