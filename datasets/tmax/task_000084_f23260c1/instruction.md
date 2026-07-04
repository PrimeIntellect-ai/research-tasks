You are a Database Administrator investigating a sudden spike in database lock contention. You have been provided with two files representing different representations of the database state:

1. A JSON document log of recent query executions: `/home/user/slow_queries.json`
   This file contains an array of JSON objects, each with `qid` (query ID string) and `exec_time_ms` (execution time in milliseconds).
2. A relational CSV mapping: `/home/user/table_locks.csv`
   This file contains comma-separated values with headers: `query_id,table_name,lock_type`. This acts as an edge list in our query-to-table dependency graph.

Your task is to identify the single most "central" table causing bottlenecks. Specifically:
1. Identify all queries from the JSON file that took strictly longer than 1000 milliseconds.
2. Cross-reference these slow queries with the CSV edge list.
3. Count how many distinct slow queries hold *any* type of lock on each table (calculating the degree centrality of tables in the subgraph of slow queries).
4. Find the table name with the highest count.
5. Write *only* the name of this bottleneck table to a new file at `/home/user/bottleneck_table.txt`.

If there is a tie, write the table name that comes first alphabetically. You should solve this entirely using a Bash pipeline (e.g., combining `jq`, `grep`, `awk`, `sort`, `uniq`, etc.).