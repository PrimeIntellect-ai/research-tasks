You are a performance engineer profiling a mathematical pipeline for structural biology. The pipeline parses structural data to extract coordinate interactions, but the matrix factorization step frequently fails with numerical instability when applied to low-resolution or modeled structures containing near-degenerate atomic coordinates.

Your task is to write a Python script that analyzes this instability, implements a regularization fix, and outputs statistical and analytical metrics.

Write a Python script at `/home/user/profile_matrix.py` that performs the following steps:

1. **Bioinformatics Parsing**: Parse the PDB file located at `/home/user/data/protein.pdb`. Extract the X, Y, and Z coordinates for all atoms where the atom name is exactly `" CA "` (Alpha Carbon). 
   * *Hint on PDB Format:* In an `ATOM` line, the atom name is at 1-indexed columns 13-16, X is at 31-38, Y is at 39-46, and Z is at 47-54.

2. **Array Manipulation**: Build an $N \times 3$ coordinate array. Compute the $N \times N$ pairwise Euclidean distance matrix $D$. From $D$, compute the affinity matrix $M$ defined as $M_{i,j} = \exp(-D_{i,j}^2 / 2)$.

3. **Numerical Stability Profiling**: Compute the condition number of $M$ (using the 2-norm). Also, compute the eigenvalues of $M$. Because of near-degenerate coordinates, the matrix is near-singular, and floating-point inaccuracies may result in small negative eigenvalues despite $M$ being positive semi-definite. Note the minimum eigenvalue.

4. **Regularization & Analytical Validation**: Apply Tikhonov regularization to stabilize the matrix: $M_{reg} = M + \lambda I$, where $\lambda = 10^{-5}$ and $I$ is the identity matrix. Calculate the eigenvalues of $M_{reg}$. Calculate the trace of $M_{reg}$ directly from its diagonal elements, and keep the top 3 largest eigenvalues of $M_{reg}$ (sorted descending).

5. **Statistical Comparison**: Perform a 2-sample Kolmogorov-Smirnov test (`scipy.stats.ks_2samp`) comparing the unregularized eigenvalues of $M$ with the regularized eigenvalues of $M_{reg}$ to see if the distribution shift is statistically distinguishable. Note the KS statistic.

6. **Reporting**: Create a JSON file at `/home/user/profiling_report.json` containing exactly the following keys and their computed values:
   * `"num_ca_atoms"`: (integer) The number of CA atoms extracted.
   * `"min_eigenvalue_unreg"`: (float) The smallest eigenvalue of the unregularized matrix $M$.
   * `"condition_number_unreg"`: (float) The condition number of $M$.
   * `"trace_reg"`: (float) The sum of the diagonal elements of $M_{reg}$.
   * `"top_3_eigenvalues_reg"`: (list of 3 floats) The three largest eigenvalues of $M_{reg}$, sorted descending.
   * `"ks_statistic"`: (float) The KS test statistic between the unregularized and regularized eigenvalue distributions.

You will need to install any necessary dependencies (like `numpy` and `scipy`) using `pip`. Execute your script to generate the report.