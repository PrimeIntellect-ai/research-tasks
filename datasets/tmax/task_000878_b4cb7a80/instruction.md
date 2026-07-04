You are assisting a data researcher who is organizing datasets and converting relational CSV data into a graph database format (Cypher). 

The researcher wrote a Rust program located in `/home/user/graph_exporter/` to export the data. Unfortunately, they made a logical error that resembles an implicit cross join: the script currently pairs *every* author with *every* paper, ignoring the actual mapping table, and prints raw, unparameterized Cypher queries.

Your task is to fix the Rust program to correctly map the relational data to a graph structure and output a parameterized Cypher query payload in JSON format.

Here is the data structure you will find in `/home/user/data/`:
1. `authors.csv` (columns: `author_id`, `name`)
2. `papers.csv` (columns: `paper_id`, `title`)
3. `authors_papers.csv` (columns: `author_id`, `paper_id`) - This is the mapping table that indicates which author actually wrote which paper.

Modify the Rust project at `/home/user/graph_exporter/src/main.rs` so that it:
1. Reads `authors_papers.csv` to find the correct relationships.
2. Generates a single parameterized Cypher query designed for batch insertion. The query must be exactly: 
   `UNWIND $batch AS row MERGE (a:Author {id: row.author_id}) MERGE (p:Paper {id: row.paper_id}) MERGE (a)-[:WROTE]->(p)`
3. Creates a JSON payload representing the query and its parameters (the valid pairs from the mapping table).
4. Saves this JSON to `/home/user/graph_exporter/output.json`.

The expected JSON format for `/home/user/graph_exporter/output.json` is:
```json
{
  "query": "UNWIND $batch AS row MERGE (a:Author {id: row.author_id}) MERGE (p:Paper {id: row.paper_id}) MERGE (a)-[:WROTE]->(p)",
  "parameters": {
    "batch": [
      {
        "author_id": 1,
        "paper_id": 101
      },
      ...
    ]
  }
}
```
*Note: Make sure the `author_id` and `paper_id` in the JSON are integers. Sort the `batch` array by `author_id` ascending, then `paper_id` ascending.*

Run the Rust program so that the `output.json` file is generated.