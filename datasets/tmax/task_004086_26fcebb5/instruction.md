You are a machine learning engineer preparing a training dataset of molecular graphs. Your pipeline requires computing a specific statistical "Graph Energy" feature for a large set of graphs. Previously, the pipeline used parallel processing to aggregate these features, but the total energy calculated varied slightly between runs due to floating-point reduction order issues (non-deterministic completion order of parallel workers). 

Your task is to write a Python script `/home/user/generate_features.py` that processes a dataset of graphs, computes their features in parallel, and performs a numerically stable, deterministic reduction.

Dataset:
The graphs are located in `/home/user/data/`. There are 100 text files named `graph_0.txt` to `graph_99.txt`.
Each file contains edge lists (two integers per line, separated by a comma, representing an undirected edge between node A and node B). Nodes are zero-indexed.

Graph Energy Formula:
For a single graph, the feature $E$ (Graph Energy) is the sum over all its nodes:
$E = \sum_{v \in V} \text{degree}(v) \times \sin(v + 1.2345)$
where $\text{degree}(v)$ is the number of edges connected to node $v$, and $v$ is the integer node ID. Note: use Python's `math.sin`.

Requirements:
1. You must use Python's `multiprocessing` module to compute the graph energies in parallel.
2. To ensure strict reproducibility and avoid floating-point drift from non-deterministic accumulation order, you MUST sort the computed graph energies by their Graph ID (from 0 to 99) before summing them up to calculate the "Total Dataset Energy".
3. Write the Total Dataset Energy to `/home/user/total_energy.txt`, rounded to exactly 8 decimal places.
4. Write the individual graph energies to `/home/user/features.csv`. The CSV must have two columns: `graph_id` and `energy`, sorted by `graph_id` in ascending order. The `energy` should also be rounded to 8 decimal places.

Run your script and ensure the output files are generated correctly.