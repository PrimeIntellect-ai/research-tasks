You are an AI assistant helping a data researcher organize and analyze a dataset of academic citations. 

The researcher has a SQLite database located at `/home/user/research_data.db`. It contains a single table representing a citation graph:
`CREATE TABLE citations (source_id INTEGER, target_id INTEGER);`
This table maps which paper (source_id) cites which other paper (target_id). 

Your task is to write a C program that interfaces with this SQLite database to perform an advanced analytical query. 

Create a C program at `/home/user/analyzer.c` that does the following:
1. Connects to `/home/user/research_data.db`.
2. Executes a single SQL query that:
   - Uses a recursive Common Table Expression (CTE) to find all papers that are transitively cited by paper ID `100` up to a maximum depth of 2 (i.e., direct citations are depth 1, citations made by those direct citations are depth 2). Do not include paper `100` itself in the output.
   - For each of these descendant papers, calculates the total number of incoming citations they receive from the *entire* database (cross-query aggregation).
   - Uses a window function (`DENSE_RANK()`) to rank these descendant papers based on their total incoming citations in descending order.
3. Writes the results to a CSV file at `/home/user/descendant_metrics.csv` in the format: `paper_id,total_incoming_citations,rank`.
4. Sorts the output primarily by `rank` (ascending) and secondarily by `paper_id` (ascending).

Compile your program using `gcc /home/user/analyzer.c -o /home/user/analyzer -lsqlite3` and run it to produce the output file. 

The final state must include the compiled executable `/home/user/analyzer` and the accurately formatted `/home/user/descendant_metrics.csv` file.