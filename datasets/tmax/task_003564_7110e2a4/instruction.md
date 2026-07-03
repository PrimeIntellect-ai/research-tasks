You are a database administrator working on optimizing a sluggish NoSQL graph query. The graph engine is currently down, and you have been provided with a raw, unindexed dump of the graph's triples in a CSV file located at `/home/user/graph.csv`. 

To restore the analytics pipeline immediately, you need to write a high-performance C utility that performs graph projection, pattern matching, and aggregation directly on this dump.

The file `/home/user/graph.csv` contains comma-separated values in the format: `Subject,Predicate,Object`. There is no header row. The fields are alphanumeric strings (up to 15 characters each).

Your task is to:
1. Write a C program at `/home/user/fast_match.c`.
2. Compile it to an executable named `/home/user/fast_match`.
3. The program must parse `/home/user/graph.csv` and match the following knowledge graph pattern:
   `?user -[VIEWS]-> ?category` AND `?category -[INCLUDES]-> ?item`
4. The program must then perform an aggregation pipeline: For each `?user`, count the total number of DISTINCT `?item`s they are connected to through this 2-hop path.
5. The program should print the aggregated results to `stdout` in the format `User,Count`, separated by a comma, with one record per line.
6. The output must be sorted alphabetically by `User`. Do not print users who have a count of 0.
7. Redirect the standard output of your compiled program to `/home/user/recommendations.csv`.

Ensure your C code is memory-safe and efficient enough to process several thousand edges.