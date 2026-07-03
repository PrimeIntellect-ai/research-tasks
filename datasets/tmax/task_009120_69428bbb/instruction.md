You are a Database Reliability Engineer (DBRE) managing a complex web of database backups. Our backup system relies on a dependency graph: certain databases must be restored before others due to cross-database foreign keys. 

You have been provided a tab-separated file at `/home/user/backups.tsv` containing the direct dependencies. Each line has the format:
`DependentDB    ParentDB`
This means `DependentDB` relies on `ParentDB` (so `ParentDB` must be restored first).

Your task is to write a C program named `/home/user/analyze_backups.c` that performs the following graph analytics and hierarchical processing:
1. Parse the `/home/user/backups.tsv` file to build a directed acyclic graph (DAG) of dependencies.
2. For every database present in the file (either as a parent or dependent), calculate its "descendant score": the total number of databases that depend on it directly or indirectly (a recursive hierarchical query).
3. Filter out any databases that have a descendant score of 0.
4. Sort the remaining databases in descending order by their descendant score. If two databases have the same score, sort them alphabetically ascending by their name.
5. "Paginate" the results by taking only the top 5 databases from the sorted list.
6. Write these top 5 databases and their scores to `/home/user/top_backups.txt` in the format `DatabaseName,Score` (one per line).

Compile your C program to `/home/user/analyze_backups` using `gcc` and execute it to generate the final text file. Do not use any external graph libraries; implement the parsing, recursive traversal, and sorting using standard C libraries (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`).