You are assisting a bioinformatics researcher who is organizing a complex web of dataset derivations. The researcher uses an older proprietary tool to find the optimal (lowest cost) transformation path between any two datasets in their pipeline. However, the source code for this tool has been lost, and they only have a stripped binary left at `/app/dataset_lineage_oracle`.

Your task is to write a Rust replacement for this tool that exactly replicates its behavior, enabling it to be integrated into a modern data-comprehension pipeline.

The oracle binary takes two arguments: a `source_dataset_id` and a `target_dataset_id`. It reads a JSON document from standard input representing the dataset graph, and outputs the shortest derivation path and its cost. 

1. Create a new Rust project at `/home/user/lineage_solver`.
2. Experiment with the `/app/dataset_lineage_oracle` binary to determine:
   - The exact JSON schema it expects on `stdin` (hint: it's a document format mapping dataset IDs to their weighted transformation dependencies).
   - The exact output format it produces for both successful paths and unreachable targets.
3. Implement the graph traversal and shortest-path computation logic (e.g., Dijkstra's algorithm) in your Rust application.
4. Ensure your implementation efficiently handles the cross-representation mapping from the JSON document input to an internal graph structure.
5. Compile your final solution in release mode. The resulting binary must be located at `/home/user/lineage_solver/target/release/lineage_solver`.

Your Rust program must be a drop-in replacement. Automated verification will run hundreds of randomly generated dataset graphs through both the oracle and your binary to ensure bit-exact output equivalence.