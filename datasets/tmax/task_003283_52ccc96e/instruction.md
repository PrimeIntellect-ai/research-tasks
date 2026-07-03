You are tasked with building a specialized data processing service in C++ to analyze an ongoing stream of transaction data using a proprietary scoring algorithm.

You have a dataset of graph-like transactions located at `/home/user/data/transactions.csv` with the following headers:
`tx_id,source_node,target_node,timestamp,amount`

We have a proprietary compiled scoring engine located at `/app/prop_scorer`. It is a stripped executable that takes two arguments: `<source_node_id>` and `<metric_value>`. It evaluates the risk score of the node based on internal logic and prints an output in an unstructured format (e.g., `[SUCCESS] Evaluation complete. Risk Metric: <score>`).

Your goal is to write and run a C++ TCP server that:
1. Listens on `127.0.0.1:8080`.
2. Accepts incoming TCP connections. Each connection will send a single line containing a `source_node` ID (as an integer), followed by a newline (`\n`).
3. Upon receiving a `source_node` ID, your service must read the CSV file and calculate a specific analytical window metric for that node: the **maximum 3-transaction rolling sum** of the `amount` column, ordered by `timestamp` ascending. (i.e., for every window of up to 3 consecutive transactions for that source node, find the sum of amounts, and then find the maximum of these sums).
4. Invoke the `/app/prop_scorer` binary, passing the requested `source_node` ID and the calculated maximum rolling sum as arguments.
5. Parse the binary's standard output to extract the numeric score.
6. Return a strictly validated JSON payload back over the TCP socket before closing the connection. The output schema must exactly match:
   `{"node": <source_node_id>, "score": <extracted_score>}\n`

Requirements:
- Your C++ code should be saved at `/home/user/server.cpp`.
- Compile it (e.g., using `g++`) and run the service in the background.
- You must use basic Linux/C++ tools; do not rely on large third-party web frameworks (standard POSIX sockets are recommended).
- Ensure the server stays running and can handle sequential requests.