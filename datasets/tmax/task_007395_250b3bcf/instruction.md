You are a Database Reliability Engineer managing backups for a monolithic application that is being decomposed. You have received a report of recurring deadlocks during concurrent restore operations and mass inserts. You suspect these deadlocks are caused by cyclic foreign key dependencies in the legacy schema.

Your task is to analyze the SQLite database backup located at `/home/user/legacy_system.db`.

You must write a Bash script at `/home/user/analyze_fks.sh` that performs the following steps:
1. Connects to `/home/user/legacy_system.db` using the `sqlite3` CLI.
2. Dynamically extracts the schema and identifies all tables and their foreign key dependencies.
3. Builds a dependency graph and identifies all tables that are part of a cyclic foreign key dependency path (e.g., Table A references Table B, Table B references Table C, Table C references Table A).
4. Groups the tables by their distinct, independent cycles (Strongly Connected Components).
5. For each distinct cycle, calculates the aggregated sum of all rows across all tables in that cycle.
6. Writes the results to a log file at `/home/user/deadlock_risk.log`.

The output in `/home/user/deadlock_risk.log` must have exactly one line per detected cycle in the following format:
`Cycle: [comma-separated alphabetically sorted list of tables in cycle] | Total Rows: [sum of rows]`

For example, if you find two separate cycles, your file should look like:
```
Cycle: categories,products,suppliers | Total Rows: 1450
Cycle: departments,employees | Total Rows: 210
```
Sort the lines in the file alphabetically by the `Cycle:` string.

Constraints & Requirements:
- You must write the solution primarily in Bash, leveraging standard Linux utilities (`awk`, `sed`, `grep`, etc.) and the `sqlite3` CLI.
- Do not use Python, Perl, or Node.js for the core graph analysis. 
- Ensure your script handles an arbitrary number of tables and cycles.
- The script should be executable (`chmod +x`).