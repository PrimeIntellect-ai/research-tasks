You are a bioinformatics analyst working on a custom sequence processing pipeline in C. You have been given a dataset containing raw observational nanopore signal intensities, but the data is in an unpivoted, sparse-like format and needs to be analyzed for periodic features.

Your objective is to write a C program that reshapes the data, extracts a specific frequency component using a Discrete Fourier Transform (DFT), constructs a similarity matrix, and factors it. 

The pipeline must perform the following steps:

1. **Data Reshaping**: Read the file `/home/user/observational_data.tsv`. It contains three columns: `seq_id` (a single character 'A', 'B', 'C', or 'D'), `time_idx` (integer from 0 to 7), and `signal` (float). 
   Reshape this into four arrays of length 8, corresponding to sequences A, B, C, and D. Assume missing time indices have a signal of 0.0.

2. **Fourier Transform**: For each of the 4 sequences, compute the magnitude of the 1st frequency bin ($k=1$) of the 8-point Discrete Fourier Transform (DFT). 
   The DFT is defined as: $X[k] = \sum_{n=0}^{7} x[n] e^{-i 2\pi k n / 8}$. 
   Calculate the magnitude as $|X[1]| = \sqrt{\text{Re}(X[1])^2 + \text{Im}(X[1])^2}$.
   Let these magnitudes be $M_A, M_B, M_C, M_D$.

3. **Matrix Construction**: Construct a 4x4 matrix $S$ where each element $S_{i,j} = M_i \times M_j$ (where indices 0,1,2,3 correspond to A,B,C,D). 
   *Note: Because this matrix is formed by the outer product of a single vector with itself, it is rank-1 and thus highly singular.*

4. **Regularization and Decomposition**: To allow for stable decomposition, add Tikhonov regularization (a ridge) by adding $\lambda = 0.1$ to the diagonal elements of $S$. Let this new matrix be $S'$.
   Compute the Cholesky decomposition of $S'$ such that $S' = L L^T$, where $L$ is a lower triangular matrix.

5. **Output**: Write the diagonal elements of $L$ ($L_{0,0}, L_{1,1}, L_{2,2}, L_{3,3}$) to `/home/user/cholesky_diag.txt`, one per line, formatted to exactly 4 decimal places (e.g., `%.4f`).

**Constraints**:
- You must use **C** as your primary language to write this program. You can use standard libraries (e.g., `<stdio.h>`, `<stdlib.h>`, `<math.h>`). 
- Compile your program using `gcc` and run it. You do not need external libraries other than `-lm`.