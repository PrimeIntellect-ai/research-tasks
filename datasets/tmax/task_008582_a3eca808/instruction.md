You are an AI assistant helping a machine learning engineer prepare training data. 

We have extracted two feature matrices from our experimental pipeline (Matrix A from the training set, Matrix B from the new test set) and saved them as CSV files. We need to detect if there is a significant distribution shift between the datasets before training our generative model. 

We will measure this by treating the normalized singular values of the matrices as probability distributions and calculating their divergence.

Your task is to write a Go program `/home/user/analysis/analyze.go` that performs the following steps:

1. **Setup Module**: Initialize a Go module in `/home/user/analysis` and use `gonum.org/v1/gonum/mat` for matrix operations.
2. **Read Data**: Parse `/home/user/data/matrix_A.csv` and `/home/user/data/matrix_B.csv`. Each file contains a 50x50 matrix of floating-point numbers without headers.
3. **Decomposition**: Compute the Singular Value Decomposition (SVD) for both Matrix A and Matrix B to extract their singular values ($s_A$ and $s_B$).
4. **Distance Metric**: 
   - Normalize $s_A$ and $s_B$ so that each set of singular values sums to 1. Let these normalized vectors be probability distributions $P$ (from A) and $Q$ (from B).
   - Compute the Symmetric Kullback-Leibler Divergence: $SymKL(P, Q) = D_{KL}(P || Q) + D_{KL}(Q || P)$, where $D_{KL}(X || Y) = \sum X_i \ln(X_i / Y_i)$.
   - Write this exact output string to `/home/user/analysis/divergence.log`: `Symmetric KL: <value>` (replace `<value>` with the computed symmetric KL divergence rounded to exactly 4 decimal places).
5. **Visualization**: Create an ASCII text-based bar chart of the **first 5 singular values of Matrix A** (the unnormalized $s_A$). 
   - Write this to `/home/user/analysis/plot.txt`.
   - Each line should represent a singular value in order.
   - Format: `Index {i}: {stars}` where `{i}` is the 0-indexed position (0 to 4), and `{stars}` is a sequence of `*` characters equal to the integer part of the singular value (e.g., if $s_A[0] = 25.7$, output 25 asterisks).

Constraints:
- You must write the solution in Go.
- Ensure that the resulting `/home/user/analysis/divergence.log` and `/home/user/analysis/plot.txt` exactly match the specified formats.