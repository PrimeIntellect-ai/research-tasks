You are a bioinformatics analyst tasked with analyzing the mutational signatures of a set of synthesized DNA sequences. You need to calculate the k-mer frequency matrix, evaluate its numerical stability via matrix decomposition, and fit a decay curve to its singular values.

Your tasks are:
1. **Scientific Software Compilation**:
   There is a C source file at `/home/user/src/kmer_counter.c`. Compile this file using `gcc` with `-O3` optimization into an executable at `/home/user/bin/kmer_counter`.

2. **Data Processing**:
   Run the compiled executable on the FASTA file located at `/home/user/data/seqs.fasta`.
   The tool takes one argument (the FASTA file) and outputs a CSV to standard output representing the 3-mer frequencies for each sequence.
   Redirect this output to `/home/user/data/matrix.csv`.

3. **Matrix Decomposition and Regression (Go)**:
   Write a Go program in `/home/user/analyze/main.go` (and initialize a Go module in that directory) that performs the following analysis:
   - Read `/home/user/data/matrix.csv` into a 64-column Dense matrix (using `gonum.org/v1/gonum/mat`). Each row represents a sequence, and each column represents a 3-mer.
   - Perform Singular Value Decomposition (SVD) on this matrix to obtain the 64 singular values ($\sigma_i$).
   - Calculate the condition number of the matrix: $\kappa = \sigma_{max} / \sigma_{min}$.
   - Assume the singular values follow an exponential decay model: $\sigma_i = A \cdot e^{-b \cdot i}$ for $i = 0, 1, \dots, 63$.
   - Perform an Ordinary Least Squares (OLS) linear regression on the transformed equation $\ln(\sigma_i) = \ln(A) - b \cdot i$ to find the parameters $A$ and $b$. Use the natural logarithm.

4. **Output**:
   Your Go program must output the results as a JSON file at `/home/user/results.json` with the following structure:
   ```json
   {
       "condition_number": 12.345,
       "A": 100.5,
       "b": 0.05
   }
   ```
   (Replace the numbers with your actual computed `float64` values).

Ensure all your code is runnable and successfully writes the JSON file.