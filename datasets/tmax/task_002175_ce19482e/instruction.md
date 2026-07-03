You are a data engineer building an ETL pipeline to transform relational transaction data into a graph representation and compute a set of analytical metrics.

Your task is to write a C++ program that reads a CSV file containing relational edge data, builds an in-memory directed graph, and performs an analytical aggregation equivalent to a windowed top-K sum.

The input file is located at `/home/user/transactions.csv` and has the following header:
`source,target,amount,timestamp`

Here are the exact requirements for the pipeline:
1. **Cross-representation mapping (Relational to Graph):** Parse the CSV and construct a directed graph where `source` and `target` are nodes, and the edge weight is determined by the `amount`. 
2. **Edge Deduplication (Max Accumulation):** There may be multiple transactions between the same `source` and `target`. You must resolve these parallel edges by keeping ONLY the edge with the maximum `amount` between any specific `(source, target)` pair (ignoring timestamps).
3. **Windowed Aggregation:** For *every* node in the graph (any node that appears as either a source or a target), compute the sum of the top 3 highest incoming edge weights (using the deduplicated edges). If a node has fewer than 3 incoming edges, sum all available incoming edge weights. If a node has no incoming edges, its sum is 0.
4. **Output Generation:** Write the results to `/home/user/node_metrics.csv` with the header `node_id,top3_in_weight_sum`. The output rows MUST be sorted alphabetically by `node_id`.

Write your C++ code in `/home/user/graph_etl.cpp`. Compile it using standard C++17 (`g++ -O3 -std=c++17 -o graph_etl graph_etl.cpp`) and run it to produce the `node_metrics.csv` file. 

Ensure your resulting CSV format exactly matches the requested header and alphabetical sorting to pass automated verification.