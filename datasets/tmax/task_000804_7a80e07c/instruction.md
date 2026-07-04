You are an AI assistant helping a researcher organize and analyze a dataset representing a citation graph. 

The researcher has an SQLite database located at `/home/user/research_data.db`. The database contains two tables:
1. `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT, `category` TEXT)
2. `citations` (`source_id` INTEGER, `target_id` INTEGER) - Represents a directed edge where `source_id` cites `target_id`.

Currently, the database is unindexed and graph queries are slow. The researcher needs a C program to optimize the database and generate a cluster-level summary based on graph centrality (specifically, in-degree centrality, which is the number of citations a paper receives).

Your task:
1. Write a C program at `/home/user/analyze_graph.c`.
2. The program must connect to `/home/user/research_data.db` using the SQLite3 C API.
3. The program must execute SQL commands to create appropriate indexes on the `citations` table to optimize querying by `target_id`. Name the index `idx_target_id`.
4. The program must then execute a query that:
   - Calculates the in-degree centrality (total citations received) for every paper.
   - Aggregates these metrics across queries/subqueries to produce a summary per `category`.
   - The summary should find the total number of citations received by all papers in each category, and the `id` of the top-cited paper in that category (if there is a tie for the top-cited paper, you can return any of the tied IDs).
5. The C program must output the results to `/home/user/summary.csv` in exactly this format, sorted alphabetically by category:
   `category,total_category_citations,top_paper_id`

For example:
```
Biology,145,102
Computer Science,250,15
Mathematics,89,42
```

Compile your C program using `gcc` and run it to produce the `summary.csv` file. Ensure the database retains the newly created index.