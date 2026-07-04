You are a data engineer building an ETL pipeline that processes financial transaction data into a graph structure. 

We have a legacy, proprietary graph analytics engine compiled as a stripped binary located at `/app/legacy_graph_oracle`. This binary expects to read graph edge lists (CSV format: `source_node,target_node,transaction_type,amount`) from standard input and computes proprietary centrality and clustering metrics. 

However, the binary is highly unstable. It crashes (segfaults) or produces garbage output when fed "corrupt" or "malicious" transaction data. Based on past incidents, we know the binary fails under specific topological anomalies (like certain types of impossible relationship cycles) and schema violations (like invalid transaction types disguised as valid ones).

Your task is to create a Python script at `/home/user/graph_sanitizer.py` that acts as a robust filter for our ETL pipeline. 

Requirements for `/home/user/graph_sanitizer.py`:
1. It must be executable from the command line as: `python3 /home/user/graph_sanitizer.py <input_csv_file>`.
2. It must analyze the graph projection and schema relationships within the input CSV.
3. It must print exactly "ACCEPT" to standard output and exit with code 0 if the graph data is perfectly safe for the legacy binary.
4. It must print exactly "REJECT" to standard output and exit with code 1 if the graph data contains topological anomalies or schema violations that would crash or exploit the legacy binary.

To help you figure out exactly what the binary rejects, you can experiment with `/app/legacy_graph_oracle`. Feed it small, crafted CSVs to reverse-engineer its constraints. You will need to apply complex joins or graph projection logic in your Python script to detect these complex structural conditions.

Ensure your Python code is highly optimized, as it will process large batches. Do not modify the binary itself.