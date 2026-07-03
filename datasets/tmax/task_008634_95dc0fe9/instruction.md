You are a machine learning engineer preparing a dataset of molecular structures for a Graph Neural Network (GNN). The raw data is provided in an HDF5 file, and you need to build a robust Rust pipeline to extract structural features, test for numerical stability, and format the output for training.

**Input Data:**
There is an HDF5 file located at `/home/user/raw_molecules.h5`. 
It contains a root group called `/graphs`. Inside this group, there are several datasets named `graph_0`, `graph_1`, etc. Each dataset is a 2D $N \times N$ matrix of floating-point numbers representing the adjacency matrix $A$ of a molecular graph.

**Task:**
Create a Rust project in `/home/user/graph_prep` that reads the HDF5 file and computes the following for each graph:
1. **Graph Algorithm (Laplacian):** Compute the unnormalized graph Laplacian $L = D - A$, where $D$ is the diagonal degree matrix ($D_{ii} = \sum_{j} A_{ij}$).
2. **Eigenvalue Extraction:** Compute the eigenvalues of $L$ and sort them in ascending order: $\lambda_0 \le \lambda_1 \le \dots \le \lambda_{N-1}$.
3. **Numerical Stability Test:** Mathematically, the smallest eigenvalue $\lambda_0$ of a valid graph Laplacian should be exactly $0$. However, due to floating-point errors or anomalous data, this might deviate. Flag the graph's stability as `stable = false` if $\lambda_0 < -10^{-5}$ or $\lambda_0 > 10^{-5}$. Otherwise, `stable = true`.
4. **Curve Fitting:** Fit a quadratic curve $y = a x^2 + b x + c$ to the eigenvalue spectrum using Ordinary Least Squares regression. Here, $x$ is the 0-based index of the eigenvalue ($0, 1, \dots, N-1$) and $y$ is the eigenvalue $\lambda_x$.

**Output:**
Your Rust program must output the extracted features to a JSON Lines file at `/home/user/features.jsonl`. 
Each line must be a valid JSON object representing one graph, with exactly these keys:
- `"graph_id"` (string, e.g., `"graph_0"`)
- `"a"` (float, the quadratic coefficient)
- `"b"` (float, the linear coefficient)
- `"c"` (float, the constant term)
- `"stable"` (boolean)

*Note on dependencies:* You are restricted to user-space tools. If you use the `hdf5` Rust crate, it is highly recommended to include the `hdf5-src` feature in your `Cargo.toml` so it compiles the C library from source without requiring root system packages. You may use crates like `nalgebra`, `ndarray`, and `serde_json`.

Compile and run your project so that the `/home/user/features.jsonl` file is fully generated.