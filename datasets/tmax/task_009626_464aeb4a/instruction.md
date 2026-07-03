You are a Database Reliability Engineer (DBRE) tasked with managing partial, consistent backups for a massive relational database. To create a consistent partial backup, whenever you back up a table, you must also back up all tables it has foreign key dependencies on, and any tables those depend on (transitive dependencies). 

You have been provided with two files in your home directory (`/home/user`):
1. `schema_fks.txt`: A space-separated list representing direct foreign key dependencies across the entire schema. Each line is formatted as `TABLE_A TABLE_B`, meaning `TABLE_A` depends on `TABLE_B` (i.e., TABLE_A has a foreign key pointing to TABLE_B).
2. `critical_tables.txt`: A list of the starting tables (one per line) that *must* be included in tonight's backup.

Your task is to write a Bash script named `/home/user/plan_backups.sh` that analyzes these relationships and performs the following tasks:

1. **Calculate the Backup Set**: Traverse the dependency graph starting from the tables in `critical_tables.txt`. Output the complete, deduplicated list of tables that must be backed up (including the critical tables themselves and all transitive dependencies). Save this alphabetically sorted list (one table per line) to `/home/user/backup_set.txt`.
2. **Identify the Core Table**: Analyze the *entire* schema graph (from `schema_fks.txt`) to find the table with the highest "in-degree" centrality—meaning the table that the highest number of *other* tables directly depend on. Save the name of this single table to `/home/user/core_table.txt`.

Ensure your script is executable and run it to generate the two required output files.

Requirements:
- Your solution must be primarily written in Bash.
- Ensure the output formats perfectly match the instructions (lowercase, sorted, one word per line).