You are helping a researcher debug a data processing pipeline for a bioinformatics simulation. The researcher has written a custom C++ tool to parse atomic coordinates from a PDB file, compute the 3x3 covariance matrix of the alpha-carbon (CA) atoms, and invert this matrix to extract structural features.

However, the pipeline is crashing on a specific synthetic peptide (`/home/user/mutant.pdb`). The atoms in this synthetic peptide are perfectly collinear, causing the covariance matrix to be singular. As a result, the matrix inversion fails (producing a division by zero / NaN because the determinant is 0).

Your tasks are to:
1. Inspect `/home/user/analyze_pca.cpp` and locate the point where the 3x3 covariance matrix `cov` is computed before its determinant and inverse are calculated.
2. Implement Tikhonov regularization in the C++ code to handle this near-singular input: specifically, add `0.0001` (1e-4) to the diagonal elements of the 3x3 covariance matrix before the determinant and inverse are calculated.
3. Compile the modified C++ code into an executable named `analyze_pca` in `/home/user/`.
4. Run the compiled executable, providing `/home/user/mutant.pdb` as the first command-line argument.
5. Save the standard output of the program (which will be the trace of the inverted matrix, formatted to 2 decimal places) into a new file at `/home/user/result.txt`.

Ensure your regularization addition is exactly `0.0001` to the diagonal to match the expected precision in the automated test.