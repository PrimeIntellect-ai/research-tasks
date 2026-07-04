You are a data analyst investigating a potential money laundering operation. You have been provided with a CSV file containing transaction records, but the relationships are complex and hidden. Your task is to process this CSV, construct a Knowledge Graph, query it to find circular transaction rings (which often indicate obfuscation or "deadlock-like" cyclic dependencies in financial systems), and perform graph analytics to identify the central coordinator.

Here is the specification for the task:

1. **Setup**:
   - The input file will be located at `/home/user/transactions.csv`. It has the columns: `tx_id`, `source_acc`, `target_acc`, `amount`, `timestamp`.
   - You must write a Python script at `/home/user/analyze_graph.py` to perform the analysis.
   - You may use `pip` to install necessary libraries (e.g., `rdflib` for SPARQL/graph representation, `networkx` for analytics, `pandas` for CSV parsing).

2. **Graph Construction**:
   - Parse the CSV and construct an RDF Knowledge Graph using `rdflib`.
   - Use the namespace `http://example.org/fraud/` (bound to prefix `ex:`).
   - Represent accounts as URIs (e.g., `ex:ACC_101`).
   - For every transaction, create a triple: `(ex:source_acc, ex:transferredTo, ex:target_acc)`. Do not worry about multiple edges between the same accounts for the graph structure; just add the triples (rdflib handles unique edges automatically).

3. **SPARQL Pattern Matching**:
   - Write and execute a SPARQL query within your Python script to find all accounts involved in exactly **3-hop circular transaction rings**. A 3-hop ring means Account A transferred to Account B, Account B transferred to Account C, and Account C transferred back to Account A. (All 3 accounts must be distinct).
   - Extract the URIs of all unique accounts that participate in at least one 3-hop ring.

4. **Graph Analytics**:
   - Extract the subgraph of these 3-hop ring participants. Create a directed graph using `networkx` containing ONLY the accounts identified in the SPARQL query as nodes, and add directed edges between them if there is an `ex:transferredTo` relationship in the full RDF graph.
   - Compute the **Degree Centrality** for the nodes in this subgraph using `networkx.degree_centrality`.

5. **Output**:
   - Identify the account URI in the subgraph with the highest degree centrality. If there's a tie, pick the one that comes first alphabetically.
   - Save your final results to `/home/user/fraud_report.json` with the following strict JSON format:
     ```json
     {
       "ring_participants": ["http://example.org/fraud/ACC_...", "http://example.org/fraud/ACC_..."],
       "mastermind": "http://example.org/fraud/ACC_..."
     }
     ```
   - The `ring_participants` list must contain all unique account URIs involved in 3-hop cycles, sorted alphabetically.
   - The `mastermind` is the single string URI of the account with the highest degree centrality in the isolated subgraph.

Ensure your script is self-contained, completely automated, and correctly outputs the required JSON file when executed via `python3 /home/user/analyze_graph.py`.