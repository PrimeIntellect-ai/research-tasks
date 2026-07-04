You are an AI assistant helping a data researcher organize and analyze a complex dataset of network interactions.

The researcher has left a snapshot of the raw data in a document database format (JSON) at `/app/raw_data.json`, but the exact relational schema they intended to use for their SQLite analysis was lost. The only surviving record of the schema is a screenshot of their notes, located at `/app/schema_info.png`.

Your task involves several stages of data comprehension, transformation, and analytical querying:

1. **Schema Reconstruction**: Read the image at `/app/schema_info.png` (Tesseract OCR is installed). It contains the definitions for two tables: one mapping nodes to their groups, and another defining the directed edges (links) and their weights.

2. **Data Model Cross-Representation Mapping**: Read the document-oriented data from `/app/raw_data.json` and load it into a new SQLite database at `/home/user/graph.db`. You must map the nested JSON structures into the relational schema you recovered from the image.
   * The JSON is structured as a list of "Group" objects. Each Group object has a `group_id` and a list of `nodes`.
   * Each node has a `node_id` and a list of `incoming_links` (each containing a `source_id` and a `weight`).

3. **Analytical Graph Querying**: The researcher needs a specific graph metric calculated: the **Intra-group Weighted Rank Sum (IWRS)** for specific nodes.
   * For a given `target_node`, look at all of its *incoming* links.
   * Filter these links to keep *only* the ones where the source node belongs to the *same* group as the `target_node`.
   * Over this filtered set of incoming links, assign a `DENSE_RANK()` based on the link's weight in descending order (highest weight gets rank 1). If there is a tie in weight, order by the source node ID in ascending order.
   * The IWRS is the sum of `(weight * dense_rank)` for all these filtered links. If a node has no incoming links from its own group, its IWRS is `0.0`.

4. **Tool Creation**: Write a Python script at `/home/user/graph_analyzer.py`.
   * It must take exactly one command-line argument: the path to the SQLite database.
   * It must read a JSON array of integer Node IDs from standard input (`stdin`).
   * It must calculate the IWRS for each Node ID in the input array.
   * It must output a JSON array of floats (the IWRS values) to standard output (`stdout`), in the exact same order as the input Node IDs.

Example usage:
```bash
echo '[102, 504]' | python3 /home/user/graph_analyzer.py /home/user/graph.db
```
Output:
```json
[45.5, 0.0]
```

Ensure your script is highly robust and performs the queries efficiently. An automated fuzzer will test your `/home/user/graph_analyzer.py` script against thousands of random Node ID combinations using a reference database to ensure your SQL window functions and joins are perfectly accurate.