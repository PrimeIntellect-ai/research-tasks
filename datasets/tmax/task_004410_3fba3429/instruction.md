You are a Machine Learning Engineer preparing training data for a new Graph Neural Network (GNN) model that predicts molecular properties. 

Our current data pipeline relies on a legacy, closed-source binary tool located at `/app/oracle_extractor`. This tool takes a molecular graph (represented as an unweighted, undirected edge list) and outputs a 5-dimensional continuous feature vector (embedding) that captures the graph's spectral topology. 

Unfortunately, `/app/oracle_extractor` is extremely slow, single-threaded, and cannot be used for our new dataset of millions of molecules. We need you to write a high-performance replacement in **Rust**.

Here is what you need to do:

1. **Analyze the Oracle**:
   The binary `/app/oracle_extractor` is stripped and takes a single graph file path as a command-line argument. The graph files contain one edge per line (e.g., `0 1` meaning an edge between node 0 and node 1). It prints 5 comma-separated floats to standard output. 
   *Hint:* The legacy documentation mentions the tool extracts the "top 5 largest singular values of the graph's Adjacency matrix". If a graph has fewer than 5 nodes, the remaining values are padded with zeros. You can use the oracle to verify this behavior and check your precision.

2. **Implement the Feature Extractor in Rust**:
   Create a new Rust project at `/home/user/rust_extractor`.
   Write a Rust program that computes these exact same 5 features for any given edge list. 
   *   You will likely need crates like `ndarray` and `ndarray-linalg` to perform the matrix decompositions (SVD).
   *   Assume nodes are indexed continuously from `0` to `N-1`, where `N` is the maximum node ID present in the file plus one.
   *   The adjacency matrix $A$ should be constructed such that $A_{i,j} = 1$ if there is an edge between $i$ and $j$, and $0$ otherwise.

3. **Process the Dataset**:
   We have placed a small sample dataset of 500 molecular graphs in the `/app/dataset/` directory (files are named `graph_0.txt` to `graph_499.txt`).
   Your Rust program must process all `.txt` files in a given directory and output the results to a CSV file.

4. **Output Format**:
   Run your Rust program on `/app/dataset/` and save the output to `/home/user/embeddings.csv`.
   The CSV must have the following header and format:
   ```csv
   filename,f1,f2,f3,f4,f5
   graph_0.txt,2.4142,1.0000,0.5123,0.0000,0.0000
   ...
   ```
   Sort the singular values in descending order (`f1` is the largest). Sort the rows alphabetically by `filename`.

We will evaluate your `/home/user/embeddings.csv` against the true values using a Mean Squared Error (MSE) metric. To succeed, your results must achieve an MSE of `< 1e-5` compared to the golden reference.