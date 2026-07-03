You are assisting a data researcher who has a large SQLite database of academic publications, but they have lost the schema documentation. Previously, the researcher wrote a Python script to calculate citation statistics by concurrently updating row counts, but it kept failing with "database is locked" (contention/deadlock) errors. 

To solve this, you need to abandon the concurrent update approach and write a robust Go program that performs cross-query aggregation on the fly. 

Here is your task:
1. Examine the SQLite database located at `/home/user/dataset.db`. You will need to reverse engineer its data model to understand how researchers, publications, authorship, and citations are stored.
2. Write a Go program at `/home/user/analyzer.go` that queries this database.
3. The Go program must calculate the following for each researcher:
   - `total_publications`: The total number of publications they have authored or co-authored.
   - `total_citations`: The total number of times any of their publications have been cited by other publications.
4. Your query must sort the results by `total_citations` in descending order. If there is a tie, sort by the researcher's full name in ascending alphabetical order.
5. The query must implement pagination to only retrieve the top 5 results (Limit 5, Offset 0).
6. The Go program must execute this as a single read-only query (using joins and aggregations) to avoid the locking issues the researcher previously faced.
7. The Go program must output the result as a formatted JSON array and save it to `/home/user/top_researchers.json`.

The JSON output should strictly follow this format:
```json
[
  {
    "researcher_id": 1,
    "full_name": "Alice Smith",
    "total_publications": 12,
    "total_citations": 45
  },
  ...
]
```

To complete this, you will need to initialize a Go module in `/home/user/`, fetch the necessary SQLite driver (e.g., `github.com/mattn/go-sqlite3`), write the code, and run it so that the final `top_researchers.json` file is produced.