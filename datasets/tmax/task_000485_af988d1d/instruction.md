You are acting as a data scientist analyzing molecular network graphs. We have a pipeline that fits a matrix factorization model to graph adjacency matrices to extract latent interaction features, but the current pipeline is broken.

There are three main issues you need to resolve:

1. **Broken Vendored Library**: We rely on a custom Python library called `graph_factor_lib` located at `/app/graph_factor_lib`. Currently, it fails to install via `pip install -e .` because its `setup.py` is misconfigured (it is missing the `numpy` include directories required to build its C-extension). You must fix `setup.py` and install the package in the active Python environment.
2. **Singular Matrix Errors**: The library performs an inversion on a graph Laplacian matrix. For our near-singular molecular graphs, this throws a `LinAlgError`. You need to patch `/app/graph_factor_lib/graph_factor_lib/solver.py` to add a small regularization term (`1e-5 * np.eye(n)`) to the matrix before inversion to prevent this crash.
3. **Pipeline Orchestration**: You must write a Bash script at `/home/user/run_pipeline.sh` that orchestrates our evaluation workflow. 
   - We have several molecular graph edge-list files in `/home/user/data/` (e.g., `mol_1.edges`, `mol_2.edges`).
   - For each `.edges` file, use `papermill` to execute the Jupyter notebook `/home/user/evaluate_model.ipynb`.
   - Pass the input file path to the notebook via the `input_graph` parameter, and output the executed notebook to `/home/user/notebooks_out/` (e.g., `mol_1_out.ipynb`).
   - The notebook automatically writes a `{basename}_metrics.txt` file (e.g., `mol_1_metrics.txt`) containing the Kullback-Leibler (KL) divergence between the true and reconstructed graph degree distributions.
   - Your Bash script must aggregate the KL divergence scores from all generated `*_metrics.txt` files and calculate the mean KL divergence, saving ONLY this final numeric mean to `/home/user/final_mean_kl.txt`.

**Expected final state**:
- `graph_factor_lib` is successfully installed and patched.
- `/home/user/run_pipeline.sh` is an executable bash script that successfully processes all `.edges` files using `papermill`.
- `/home/user/final_mean_kl.txt` exists and contains a single floating-point number representing the mean KL divergence across all processed graphs. To succeed, this mean must be less than 0.05.