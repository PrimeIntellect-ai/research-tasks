You are a database reliability engineer tasked with rebuilding our legacy backup validation pipeline. We have a nightly backup system that exports our infrastructure dependency graph from a relational database into flat CSV files (a `nodes.csv` and an `edges.csv`). 

Historically, a proprietary C++ utility was used to calculate "cluster integrity partitions" from the `edges.csv` file. This was critical to ensure that our backup data wasn't fragmented before archiving. We lost the source code for this utility during a recent migration, but we recovered a stripped binary artifact from an old server.

Your task is to write a replacement script that perfectly replicates the behavior of this binary so we can safely deprecate it.

Here is the setup:
1. The proprietary binary is located at `/app/cluster_verifier`. It is a stripped ELF binary.
2. The binary takes two arguments: `--in <input_edges.csv>` and `--out <output_metrics.json>`.
3. The input CSV is a headerless file containing edge connections in the format `source_id,target_id`.
4. The output is a JSON file mapping each `node_id` (as a string) to an integer representing its "cluster partition ID".

You need to:
1. Investigate the `/app/cluster_verifier` binary to determine exactly what graph algorithm it uses to compute the cluster partition IDs. (You can use `strace`, `strings`, `ltrace`, or just black-box test it with dummy CSV files).
2. Write a multi-language implementation (e.g., Python, since it's well-suited for graph processing) located at `/home/user/verify_clusters.py`.
3. Your script must accept the exact same arguments: `--in <input_edges.csv> --out <output_metrics.json>`.
4. Your script's output must be BIT-EXACT equivalent to the binary's output for any valid graph input.
5. Your script should efficiently handle graphs up to 100,000 nodes using appropriate data structures and index mapping.

Please test your implementation thoroughly against the binary before completing the task.