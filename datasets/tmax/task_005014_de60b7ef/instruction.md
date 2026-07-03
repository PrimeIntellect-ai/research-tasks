You are a Database Reliability Engineer. Your task is to manage database backups by parsing a knowledge graph of our database dependencies and generating an execution script.

You have been provided with an N-Triples file at `/home/user/db_graph.nt` that models our databases, their backup statuses, sizes, and dependency chains. 

The graph uses the following predicates:
- `<http://dbre/dependsOn>`: Indicates that the subject database depends on the object database. Therefore, the object database MUST be backed up BEFORE the subject database.
- `<http://dbre/lastBackupStatus>`: The string literal value is the status of the last backup (e.g., "SUCCESS", "FAILED", "MISSING").
- `<http://dbre/dbSize>`: The integer literal value is the size of the database in gigabytes.

Your objectives:
1. Identify all databases that DO NOT have a `<http://dbre/lastBackupStatus>` of `"SUCCESS"`. (i.e., they are `"FAILED"` or `"MISSING"`).
2. Calculate the total size (in GB) of all these identified databases combined. Write this single integer to `/home/user/total_backup_size.txt`.
3. Create a bash script at `/home/user/execute_backups.sh`. This script must:
   - Include a shebang (`#!/bin/bash`).
   - Be executable.
   - Contain exactly one execution line per identified database in the format: `/usr/local/bin/backup_tool --database [DB_NAME]`
   - The execution order must represent a valid topological sort based on the `<http://dbre/dependsOn>` relationships of the IDENTIFIED databases. (If identified DB A depends on identified DB B, the backup command for B must appear before A in the script).

Note: The `[DB_NAME]` is the final part of the URI. For example, for `<http://dbre/db/UserDB>`, the DB_NAME is `UserDB`. Use Bash utilities (`awk`, `grep`, `tsort`, `join`, etc.) to accomplish this. You do not need to install any external graph-processing libraries.