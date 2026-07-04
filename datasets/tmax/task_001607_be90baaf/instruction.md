I'm a machine learning engineer working on a molecular property prediction model, and I need your help reverse-engineering and reimplementing a legacy graph processing tool. 

We have a legacy C++ tool, compiled as a stripped binary located at `/app/gcn_propagate`, which computes a specific graph-based feature for our molecules. Unfortunately, the source code is lost, and we need to reimplement its exact behavior to integrate it into our modern Python/C++ ML pipeline.

Your task is to write a program (you may use Python, C++, or Rust) that takes the exact same inputs and produces the exact same outputs as the `/app/gcn_propagate` binary.

Here is what we know about the legacy binary:
1. It is invoked as: `/app/gcn_propagate <edges.csv> <features.csv>`
2. `edges.csv` contains undirected edges of a molecular graph, with two columns: `source,target` (integer node IDs).
3. `features.csv` contains initial node features, with two columns: `node_id,feature` (floating-point numbers).
4. The binary outputs to stdout the computed scores in the format `node_id,score` (floating point, 6 decimal places), sorted by `node_id`.
5. The algorithm performs exactly ONE step of a Graph Convolutional Network (GCN)-like message passing algorithm, but we aren't sure of the exact normalization factor it uses (e.g., symmetric normalized Laplacian, random walk, etc.). 
6. You will need to test the binary with some dummy data to deduce the exact normalization formula and numerical types it uses, ensuring your reimplementation is numerically stable and matches the binary's output bit-for-bit (up to the 6 decimal places printed).

Please write your reimplementation to `/home/user/my_propagate.py` (or `.cpp`/`.rs` if you choose a compiled language, along with a build script so we can compile it). It must accept the same two file path arguments and print the exact same output. 

Ensure your environment is properly managed and any dependencies you need (like `numpy` or `scipy`) are installed.