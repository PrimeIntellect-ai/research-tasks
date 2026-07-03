You are assisting a compliance officer auditing a financial transaction system for potential money laundering rings. The system's raw audit logs have been exported into a document-store format, simulated here as a SQLite database containing raw JSON objects.

You have been provided with the database at `/home/user/audit.db`. It contains a single table `raw_events` with a single column `document` (TEXT), which holds JSON strings representing system events.

Your objectives are:
1. **Reverse Engineer & Extract**: Inspect the JSON documents to understand the schema. Identify the fields representing the source account, destination account, transaction amount, and event status. You only care about events where the transaction was "completed" and the type was a "transfer".
2. **Optimize**: The compliance officer needs to run frequent aggregations on this data. Create a SQL script at `/home/user/optimize.sql` that creates an index (using SQLite's expression-based indexes or generated columns) on the source and destination account fields to speed up extraction.
3. **Graph Analytics**: Write a Python script at `/home/user/analyze.py` that reads the completed transfers from the database and builds a directed graph of the transactions (Nodes = accounts, Edges = transfers). 
4. **Identify the Suspect**: Using the `networkx` library, calculate the PageRank of all nodes (using default parameters). Find the account that has the highest PageRank score *among all accounts that are part of at least one directed cycle* (a money laundering ring). 

Save the final identified suspect and their PageRank score to `/home/user/suspect.json` in the exact following format:
```json
{
  "suspect_account": "ACT_...",
  "pagerank_score": 0.0000
}
```
*(Round the PageRank score to 4 decimal places).*

Ensure your Python script actually executes the extraction and analysis, and writes the JSON file. You may install any necessary Python packages (like `networkx` or `pandas`) using `pip`.