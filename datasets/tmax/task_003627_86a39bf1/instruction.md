You are a data analyst investigating a series of transaction networks. We have extracted transaction subgraphs into separate CSV files. Some of these subgraphs represent normal user behavior, while others represent coordinated fraud rings (sybil attacks). 

Your objective is to build a Python-based detection script that correctly identifies whether a given transaction CSV represents a fraudulent subgraph or a normal one. 

**Task Requirements:**

1. **Fix the Vendored Library:**
   We have vendored a specialized graphing library at `/app/vendored/py-graph-ext-1.2/`. You must install it using `pip install -e /app/vendored/py-graph-ext-1.2/`. However, the installation or runtime is currently failing due to a deliberate misconfiguration introduced during vendoring. You must diagnose and fix this package so you can import and use `py_graph_ext` in your script.

2. **Database & SQL Operations:**
   For each CSV file, load the data (`source_id`, `target_id`, `amount`, `timestamp`) into an in-memory SQLite database.
   Write an optimized parameterized SQL query using **window functions** to compute the "transaction velocity" for every edge. We define transaction velocity as the cumulative sum of `amount` for the `source_id` within the 60 minutes preceding (and including) the current transaction's `timestamp`. 
   *Note: Ensure your SQLite schema includes appropriate indexes to make this window aggregation efficient.*

3. **Graph Analytics:**
   Load the nodes and edges into a `py_graph_ext.Graph`. Use the library to compute the **Betweenness Centrality** of all nodes in the CSV.

4. **Detector Implementation:**
   Create a Python script at `/home/user/detector.py`. 
   The script must accept a single command-line argument: the absolute path to a CSV file.
   The script should process the CSV using the SQL and Graph techniques above, and print exactly one line to `stdout`:
   - Print `FRAUD` if the graph is deemed fraudulent.
   - Print `NORMAL` if the graph is deemed normal.
   
   *Heuristic for Fraud:* A graph is fraudulent if **any** node in the graph has a Betweenness Centrality > 0.45 AND **any** transaction in the network has a 60-minute transaction velocity > 10,000. Otherwise, it is normal.

5. **Validation:**
   Your script must successfully classify the CSVs in our labeled test sets. We have provided some sample data in `/app/corpus/clean_samples/` and `/app/corpus/evil_samples/` for you to test your logic locally. 

When you have finished creating `/home/user/detector.py`, create a file named `/home/user/DONE` to indicate task completion.