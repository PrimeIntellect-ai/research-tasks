You are acting as a data analyst and systems engineer. We have a legacy, proprietary graph analysis tool located at `/app/graph_oracle`. This tool processes large CSV files representing a knowledge graph and performs cross-query aggregations based on path patterns. 

Because the vendor has gone out of business, we only have this stripped, pre-compiled binary. We need to replace it with a highly performant, open-source implementation written in Rust.

Your objective is to reverse-engineer the logic of the `/app/graph_oracle` binary and write a Rust program that behaves **exactly** like it.

Here is what we know about the oracle:
1. It is invoked with two positional arguments: the path to a nodes CSV file and the path to an edges CSV file. 
   Example: `/app/graph_oracle /home/user/sample_data/nodes.csv /home/user/sample_data/edges.csv`
2. It reads aggregation queries from standard input (`stdin`), one per line.
3. It prints the result of each query to standard output (`stdout`), one per line.
4. The schema for the nodes CSV is `node_id,weight` (where node_id is a string and weight is an integer).
5. The schema for the edges CSV is `source_id,target_id,edge_type` (directed edges).

To help you get started, I have placed some small sample CSV files in `/home/user/sample_data/`. You should run the oracle, feed it various queries, analyze its output, and deduce the graph pattern matching and aggregation logic it uses.

Once you have figured out the exact algorithm:
1. Initialize a new Rust project at `/home/user/graph_tool`.
2. Write the Rust implementation that parses the CSVs, builds an efficient in-memory graph, and processes standard input exactly like the oracle.
3. Build your project in release mode. The final executable must be located at `/home/user/graph_tool/target/release/graph_tool`.

Your replacement tool will be rigorously tested by an automated fuzzer against the original oracle using massive, randomized graph datasets and complex path pipelines. It must produce identical output (byte-for-byte) and be robust against missing nodes, invalid paths, and empty lines. 

Make sure your program terminates cleanly when `stdin` is closed (EOF). Console output strictly matching the oracle is required for the tool to be verified. Do not print extraneous debugging information to `stdout`.