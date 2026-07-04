As a compliance officer auditing our financial networks, I need you to analyze a heterogeneous data dump of corporate entities, ownership structures, and financial transactions to identify potential money laundering rings. 

The IT team provided a NoSQL JSONL export at `/home/user/audit_data.jsonl`. The file contains mixed document types. You must reverse-engineer the schema, aggregate the transaction data, project it into a graph model, and query it for specific cyclic patterns.

Here are the requirements for the analysis:
1. **Data Aggregation**: Parse the JSONL file. Extract ownership records and transaction records. You must aggregate the total transaction amount sent from any entity `X` to any entity `Y` across all transaction records.
2. **Graph Materialization**: Construct a directed graph representing the flow of control and money. Create a directed edge from entity `X` to entity `Y` if AT LEAST ONE of the following is true:
   - `X` holds an ownership stake strictly greater than `50%` in `Y`.
   - The *total aggregated* transaction amount sent from `X` to `Y` is strictly greater than `$1,000,000`.
3. **Graph Query**: We define a "suspicious ring" as a Strongly Connected Component (SCC) in this graph that contains **3 or more distinct entities**. (A strongly connected component is a maximal subgraph where for every pair of vertices U, V, there is a directed path from U to V and from V to U).
4. **Export**: Write the identified suspicious rings to a CSV file located at `/home/user/flagged_rings.csv`. 
   - Each line in the CSV must represent one suspicious ring.
   - The entities within each line must be comma-separated and sorted alphabetically (e.g., `CorpA,CorpB,CorpC`).
   - The lines themselves must be sorted alphabetically by the first entity in the row.
   - Do not include headers or quotes.

You may write a Python script to accomplish this. You can use standard libraries or install packages like `networkx` via pip if you prefer. Ensure your final output exactly matches the requested format at `/home/user/flagged_rings.csv`.