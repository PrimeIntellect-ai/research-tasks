You are a Database Reliability Engineer. We have a custom C utility, `backup_planner.c`, that we use to determine the backup order and dependencies of our database clusters. Our databases have complex dependencies (e.g., the web database relies on the users database, which relies on auth).

We store these dependencies in a directed graph file located at `/home/user/db_graph.txt`. Each line contains two space-separated strings: `DEPENDENT_DB DEPENDENCY_DB`. 

Recently, we added a new dependency that created a multiple-path structure (a DAG with shared dependencies, and possibly cycles). When we run our `backup_planner` utility, it either hangs or outputs thousands of duplicate lines. The original developer accidentally implemented a naive recursive graph traversal that doesn't track visited nodes, simulating an implicit cross join / combinatorial explosion of paths.

Your task:
1. Fix the C code in `/home/user/backup_planner.c` so that it correctly traverses the graph using DFS or BFS, tracks visited nodes, and avoids infinite loops or duplicate outputs.
2. The program must accept a starting database name as a command-line argument and print all databases that need to be backed up (i.e., all reachable nodes in the dependency graph, including the starting node itself), each printed on a new line.
3. Compile the fixed program to `/home/user/backup_planner`.
4. Run the utility for the starting database `DB_WEB`.
5. Sort the output alphabetically and save it to `/home/user/backup_plan.txt`.

Ensure `/home/user/backup_plan.txt` contains exactly the unique, reachable database names, one per line, sorted alphabetically.