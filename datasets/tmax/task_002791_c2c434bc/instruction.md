You are acting as a data engineer tasked with analyzing an ETL pipeline's table lineage. 

You have been provided with a lineage extract in TSV format at `/home/user/etl_lineage.tsv`. Each line contains two columns separated by a tab (`\t`), representing a dependency where data flows from the `Source_Table` to the `Target_Table`.

Your task is to:
1. Write a C program at `/home/user/find_path.c` that reads the TSV data from standard input (stdin).
2. The program must build a directed graph from this data and use a graph traversal algorithm (like Breadth-First Search) to compute the shortest dependency path from `raw_users` to `mart_revenue`.
3. Compile your program to an executable named `/home/user/find_path` using standard `gcc`.
4. Pipe the contents of `/home/user/etl_lineage.tsv` into your compiled executable.
5. Your program should write the resulting shortest path to `/home/user/path_result.txt`. The output must be a single line containing the exact table names in order from start to finish, separated by commas without spaces (e.g., `raw_users,table_A,table_B,mart_revenue`).

Assume table names are at most 50 characters long, and there are fewer than 100 unique tables. If multiple paths have the same shortest length, any of them is acceptable (though the provided dataset has a unique shortest path).