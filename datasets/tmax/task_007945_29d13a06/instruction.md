You are a Database Administrator working on query optimization and result processing. We have recently executed queries across three different database systems (a relational DB, a graph DB, and a document store) to extract user metrics. You need to write a Go program that performs cross-representation mapping to join and process these extracted datasets into a unified optimization report.

The exported datasets are located in `/home/user/data/`:
1. **`/home/user/data/relational.csv`**: Contains the results of a complex SQL join.
   - Format: CSV
   - Columns: `cust_id` (string), `ltv` (float), `region` (string)
2. **`/home/user/data/graph.json`**: Contains the output of a Cypher PageRank query on our user graph.
   - Format: JSON Array of Objects
   - Fields: `node_id` (string, corresponds to cust_id), `page_rank` (float), `community` (int)
3. **`/home/user/data/documents.jsonl`**: Contains document snippets from our NoSQL user preferences store.
   - Format: JSON Lines (JSONL), one JSON object per line.
   - Fields: `_id` (string, corresponds to cust_id), `metadata` (object containing `is_active` (boolean) and `loyalty_tier` (string))

Your task:
Write a Go program located at `/home/user/process_results.go` that reads these three files, performs an inner join on the customer ID (`cust_id` == `node_id` == `_id`), and applies the following filtering logic:
- `ltv >= 500.0`
- `page_rank >= 0.15`
- `is_active == true`

For the matching records, calculate a final `Score` defined as `ltv * page_rank`.

The Go program must output the final results to `/home/user/unified_results.csv`.
The output CSV must:
1. Include a header row: `Customer_ID,Region,Loyalty_Tier,Score`
2. Round the `Score` to exactly 2 decimal places (e.g., `120.00`).
3. Be sorted by `Score` in descending order. If there is a tie, sort by `Customer_ID` in ascending alphabetical order.

Constraints:
- Use only the Go standard library (no third-party packages).
- You must write the Go code, compile it, and run it to produce the output file.