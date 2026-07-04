You are a Database Reliability Engineer investigating a backup failure caused by a transaction deadlock in your company's graph database. 

You have two files provided in your home directory:
1. `/home/user/graph_export.json` - A partial graph database backup in JSON format containing "nodes" (with "id" and "label") and "edges" (with "source", "target", and "type").
2. `/home/user/db_error.log` - A database error log containing the deadlock exception and the two concurrent Cypher queries that caused it.

Your task is to reverse-engineer the graph schema and identify the conflicting relationship type causing the deadlock. Write a Bash script or run shell commands to perform the following:
1. Parse the `graph_export.json` file to extract all unique Node Labels.
2. Parse the `graph_export.json` file to extract all unique Edge Types.
3. Analyze the Cypher queries in `db_error.log` to determine which Edge Type is being concurrently modified (SET) by both deadlocked queries.

Output your findings to a file named `/home/user/deadlock_report.txt` with exactly three lines:
Line 1: A comma-separated, alphabetically sorted list of all unique Node Labels in the graph.
Line 2: A comma-separated, alphabetically sorted list of all unique Edge Types in the graph.
Line 3: The exact name of the Edge Type that is being modified in both deadlocked Cypher queries.

Example of expected `/home/user/deadlock_report.txt` format:
Account,Database,User
CONNECTS,OWNS,READS
OWNS