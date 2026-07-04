You are a data engineer working on a localized ETL pipeline. You need to combine organizational structure data stored as an RDF graph with transactional sales data stored in an SQLite database.

We have two data sources in your home directory (`/home/user/`):
1. `org_graph.ttl`: An RDF Turtle file containing the company's reporting hierarchy. 
2. `sales.db`: An SQLite database containing a `transactions` table with columns: `id` (INTEGER), `employee_name` (TEXT), `sale_date` (DATE), and `amount` (REAL).

Your task is to write a Python script at `/home/user/etl_summary.py` that performs the following steps:

1. **Graph Querying**: Use `rdflib` to execute a SPARQL query against `org_graph.ttl`. You need to find "Alice" and all employees who report directly or indirectly to Alice (i.e., her entire reporting subgraph). The ontology uses `http://example.org/manages` to denote a management relationship (e.g., `<Manager> <http://example.org/manages> <Subordinate>`). Note: Construct your SPARQL query carefully to handle transitive relationships (using property paths).

2. **Window Functions & SQL Aggregation**: Connect to `sales.db`. Write a parameterized SQL query using Window Functions to calculate the 3-day rolling average of sales `amount` for each employee, ordered by `sale_date` ascending. Specifically, for each transaction, the rolling average should be calculated over the current row and the 2 preceding rows for that specific employee. 

3. **Cross-Query Aggregation**: For each employee identified in the SPARQL graph query (including Alice herself), find their *chronologically latest* transaction in the SQLite results and extract its 3-day rolling average. 

4. **Summarization**: Sum these final rolling averages together.

5. **Output**: Write the final aggregated result to `/home/user/result.json` in the exact following format:
```json
{
  "manager": "Alice",
  "subgraph_members": ["Alice", "Bob", ...], 
  "total_latest_rolling_avg": 123.45
}
```
*Note: Sort the `subgraph_members` list alphabetically in the JSON output. Round the `total_latest_rolling_avg` to 2 decimal places.*

Ensure your script is self-contained and executes successfully when run via `python3 /home/user/etl_summary.py`. You may install `rdflib` if needed.