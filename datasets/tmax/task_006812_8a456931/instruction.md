You are a bioinformatics analyst working on k-mer sequence transition networks. We are modeling the transitions between sequence motifs as a Markov chain. 

You have been provided with a directory `/home/user/motif_analysis` containing a transition matrix `transition_matrix.csv` representing the directed graph of motif transitions.

There is a provided script `/home/user/motif_analysis/solve_steady.py` that attempts to find the steady-state distribution $\pi$ (where $P^T \pi = \pi$) by solving the linear equation $(P^T - I)\pi = 0$. However, it currently uses standard matrix inversion (`np.linalg.inv`), which fails with a `LinAlgError` because the matrix is near-singular/singular (it represents a graph with a specific topological structure).

Your task is to write a bash script `/home/user/motif_analysis/run_pipeline.sh` that does the following:
1. Replaces or fixes the steady-state solver to use Singular Value Decomposition (SVD) or an eigendecomposition to correctly handle the singular matrix and find the null space of $P^T - I$. 
2. Normalizes the resulting vector so that its components sum to 1 (representing probabilities).
3. Performs an analytical validation step within the pipeline: it must verify that the residual $||P^T \pi - \pi||_2$ is less than $10^{-6}$.
4. Outputs the final, validated steady-state distribution as a single comma-separated line of 10 numbers to `/home/user/motif_analysis/steady_state.csv`.

Ensure your bash script handles the entire workflow when executed. You can embed a corrected Python script within your bash script using a heredoc, or modify the existing one.

File constraints:
- Input matrix: `/home/user/motif_analysis/transition_matrix.csv` (no header, 10x10 matrix of floats)
- Output file: `/home/user/motif_analysis/steady_state.csv`
- Pipeline script: `/home/user/motif_analysis/run_pipeline.sh` (must be executable and orchestrate the process)