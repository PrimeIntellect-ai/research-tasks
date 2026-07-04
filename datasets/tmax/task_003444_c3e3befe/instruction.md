You are a data engineer tasked with fixing a broken ETL pipeline and writing a robust data retrieval tool.

We have an SQLite database at `/app/graph.db` containing two tables:
1. `nodes(id INTEGER PRIMARY KEY, name TEXT)`
2. `edges(source_id INTEGER, target_id INTEGER)`

Due to a recent storage failure during an ETL job, one of the indexes in the database became corrupted. Because of this, certain queries are returning stale or incorrect rows.
Your first task is to diagnose and fix the database corruption in `/app/graph.db` (do not delete the database, just repair the indexes so that `PRAGMA integrity_check;` passes and queries work correctly).

Second, we received an audio brief from the data science team detailing a specific graph centrality metric they want to use for an upcoming API. The brief is located at `/app/requirements.wav`. You will need to transcribe or listen to this audio to understand the exact formula for the "node score" and the required sorting order.

Finally, write a Go program that implements this requirement.
Save your code at `/home/user/query_graph.go` and compile it to `/home/user/query_graph`.

The Go binary must accept exactly three command-line arguments in this order:
1. `limit` (integer): The maximum number of results to return.
2. `offset` (integer): The number of results to skip.
3. `min_score` (integer): The minimum node score to include in the results.

Your program should:
1. Connect to `/app/graph.db`.
2. Compute the score for each node according to the formula specified in the audio brief.
3. Filter out any nodes with a score strictly less than `min_score`.
4. Sort the results exactly as specified in the audio brief.
5. Apply the `limit` and `offset` for pagination.
6. Output the results to standard output as a valid JSON array of objects, where each object has the keys: `id` (integer), `name` (string), and `score` (integer). Do not print anything else.

Make sure your binary is statically compiled or runnable in the current environment, and handles edge cases (like nodes with no edges) gracefully.