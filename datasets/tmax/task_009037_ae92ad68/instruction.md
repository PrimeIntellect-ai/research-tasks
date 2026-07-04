You are acting as a compliance officer auditing an internal company system. We have been provided an SQLite database file at `/home/user/audit.db` which contains tables related to users, departments, IT assets, and access permissions. Unfortunately, the schema is entirely undocumented, so you will need to inspect the database to understand the tables, columns, and their relationships.

Your task is to identify Segregation of Duties (SoD) violations. A violation occurs when:
1. A user has a record granting them access to an asset.
2. That asset has a classification of 'RESTRICTED'.
3. The user's assigned department does NOT match the department that owns the asset.
4. The user's role is NOT 'AUDITOR'.

Write a Python script at `/home/user/find_violations.py` that connects to this database, performs the necessary schema analysis and joins, and identifies the user IDs (integers) of all users who violate the above policy.

Your Python script must execute this logic and output the violating user IDs to a file located at `/home/user/violations.txt`. 
The output file must contain exactly one user ID per line, sorted in ascending numerical order. No other text or characters should be present in the file.