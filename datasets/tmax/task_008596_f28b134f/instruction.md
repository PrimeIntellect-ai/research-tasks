You are a data engineer tasked with building an ETL pipeline to analyze transaction locks and detect deadlock-prone bottlenecks via a "Wait-For" graph.

You are provided with a raw CSV dataset of database lock events at `/home/user/locks.csv`. 
The CSV has the following columns: `tx_id` (integer), `resource_id` (string), `status` (string, either 'GRANTED' or 'WAITING').

Your objective is to write a Python script (using only standard libraries like `sqlite3`, `json`, `csv`) that performs the following steps:

1. **Database Initialization & Ingestion:**
   Create an SQLite database at `/home/user/etl.db`. Create a table named `lock_events` and load the data from `locks.csv` into it.

2. **Index Strategy:**
   Create appropriate indexes on the `lock_events` table to optimize the querying of the wait-for graph.

3. **Graph Projection & Window Aggregation:**
   Execute a SQL query that materializes a Wait-For Graph. A directed edge exists from Transaction A to Transaction B if A has a 'WAITING' status for a `resource_id` that B currently holds with a 'GRANTED' status.
   Using SQL Window Functions, calculate a `blocking_score` for each transaction that currently holds at least one lock or is waiting. 
   - `blocking_score` is defined as the count of *distinct* `tx_id`s that are waiting directly on the given transaction. If nobody is waiting on a transaction, its score is 0.
   - Assign a `rank` to each transaction based on its `blocking_score` in descending order. In case of ties, order by `tx_id` ascending.

4. **Pagination, Filtering & Schema Validation:**
   Extract only the top 5 transactions (Ranks 1 through 5).
   Format the results into a JSON file at `/home/user/report.json`. 
   
   The output JSON must strictly adhere to this schema (your Python code must ensure the types are correct before dumping):
   ```json
   {
     "type": "object",
     "properties": {
       "top_blockers": {
         "type": "array",
         "items": {
           "type": "object",
           "properties": {
             "rank": { "type": "integer" },
             "tx_id": { "type": "integer" },
             "blocking_score": { "type": "integer" }
           },
           "required": ["rank", "tx_id", "blocking_score"]
         }
       }
     },
     "required": ["top_blockers"]
   }
   ```

Do not install any external pip packages (like `pandas` or `jsonschema`), rely purely on Python's built-in libraries. Ensure the final `report.json` is perfectly formatted.