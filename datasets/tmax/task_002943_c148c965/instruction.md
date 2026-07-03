You are assisting a researcher in organizing and analyzing a dataset of academic papers. The researcher has provided an SQLite database at `/home/user/papers.db` containing a citation graph and document-like metadata.

The database has the following schema:
```sql
CREATE TABLE papers (
    id INTEGER PRIMARY KEY,
    title TEXT,
    year INTEGER,
    metadata_json TEXT -- contains JSON like {"domain": "Computer Science", "keywords": [...]}
);

CREATE TABLE citations (
    citing_id INTEGER,
    cited_id INTEGER
);
```

Your task is to write a C++ program at `/home/user/analyze_citations.cpp` that performs the following steps:
1. Connects to `/home/user/papers.db` using the SQLite3 C/C++ API.
2. Creates an optimized index (or multiple indexes) on the `citations` table to speed up bottom-up hierarchical queries (i.e., finding which papers cite a given paper).
3. Uses a Recursive Common Table Expression (CTE) to find all papers that transitively cite the paper with `id = 1`, up to a maximum depth of 3. (Depth 1 = papers directly citing paper 1; Depth 2 = papers citing Depth 1 papers, etc.).
4. Extracts the `domain` string value from the `metadata_json` column for each of these citing papers using SQLite's JSON functions.
5. Performs cross-query aggregation to summarize the data. The program must calculate the count of citing papers grouped by `depth` and `domain`.
6. Materializes the graph projection summary by writing the results to a CSV file at `/home/user/citation_summary.csv`.

The CSV file must have the following exact header and format:
```csv
depth,domain,count
1,Computer Science,5
1,Physics,2
2,Biology,10
...
```
Sort the CSV rows ascending by `depth`, then ascending by `domain` alphabetically.

Requirements:
- Do not modify the existing data in the tables, only create indexes.
- Compile your program using `g++ -O3 -std=c++17 /home/user/analyze_citations.cpp -lsqlite3 -o /home/user/analyze_citations`.
- Run your compiled program to generate `/home/user/citation_summary.csv`.
- Make sure to handle potential errors (e.g., file writing, database execution).