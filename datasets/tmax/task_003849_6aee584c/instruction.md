You are an AI assistant helping a data researcher organize and query a large dependency graph of scientific datasets.

The researcher has an SQLite database at `/home/user/datasets.db` representing a directed graph of datasets. 
The database has two tables:
1. `datasets` (`id` INTEGER PRIMARY KEY, `name` TEXT, `size_mb` INTEGER, `domain` TEXT)
2. `dependencies` (`source_id` INTEGER, `target_id` INTEGER) - This means the dataset with `source_id` *depends on* the dataset with `target_id`.

Your task is to write a Go program that traverses this graph to find the largest downstream consumers of a specific dataset. 
Specifically, do the following:

1. **Database Optimization**: Before querying, use the `sqlite3` CLI to create indexes on the database that will optimize recursive graph traversals (specifically looking up what depends on a given target) and filtering/sorting by domain and size. 

2. **Go Script**: Write a Go script at `/home/user/graph_query.go` that:
   - Uses `database/sql` and the `github.com/mattn/go-sqlite3` driver.
   - Takes a dataset name as its first command-line argument.
   - Uses a **parameterized query** containing a Recursive Common Table Expression (CTE) to find all datasets that depend on the given dataset, either directly or indirectly (a transitive closure graph query).
   - Joins the result with the `datasets` table to filter the results to only include datasets in the "Genomics" `domain`.
   - Sorts the resulting datasets by `size_mb` in descending order.
   - Paginates the results to return only the top 3 largest datasets.

3. **Execution**: Run your Go script for the target dataset `"Base_Sequences"` and redirect its output (just the dataset names, one per line) to `/home/user/top_consumers.txt`.

Ensure your Go code is properly formatted and handles database connections and errors robustly.