You are a data engineer working on an ETL pipeline that processes data from a graph database. The database administrators have provided you with a raw data extract and a query execution plan for a notoriously slow query. You need to process the data using Go, optimize the conceptual query, and analyze the execution plan.

All your work will be in the `/home/user/etl` directory. 

**Part 1: Result Processing with Go**
You have a raw output file at `/home/user/etl/raw_graph_results.json`. This file contains a JSON array of objects representing authors. Each object has the following keys: `author_id` (string), `name` (string), `pagerank` (float), and `trust_score` (float).
Write a Go script at `/home/user/etl/process.go` that does the following:
1. Reads the JSON data from `raw_graph_results.json`.
2. Filters out any authors who have a `trust_score` strictly less than `0.6`.
3. Sorts the remaining authors by `pagerank` in **descending** order. If two authors have the exact same `pagerank`, sort them by `author_id` in **ascending** alphabetical order.
4. Paginates the filtered and sorted list with a page size of **5**.
5. Extracts **Page 3** (using 1-based indexing, i.e., items 11 through 15).
6. Writes the resulting Page 3 data as a formatted JSON array to `/home/user/etl/page_3.json` (indent with 2 spaces). 
Compile and run your script to generate the output file.

**Part 2: Query Plan Analysis**
Review the database execution plan provided in `/home/user/etl/query_plan.txt`.
Identify the operation (the value in the "Operator" column) that produces the highest number of "EstimatedRows".
Write the exact name of this operator (e.g., `NodeIndexSeek`) to `/home/user/etl/bottleneck.txt`.

**Part 3: Cypher Query Generation**
The raw data was originally extracted using a poorly written Cypher query. 
Write a new, correct Cypher query and save it to `/home/user/etl/query.cypher`.
The query must:
1. Match `Person` nodes connected to `Article` nodes via a `WROTE` relationship.
2. Filter for `Article` nodes where the `publish_year` property is strictly greater than `2023`.
3. Return the `Person` node's properties: `id` as `author_id`, `name`, `pagerank`, and `trust_score`.

Ensure all requested files (`process.go`, `page_3.json`, `bottleneck.txt`, `query.cypher`) exist in `/home/user/etl` before finishing.