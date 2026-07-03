You are a machine learning engineer preparing biological sequence data to train a new model. You need to extract k-mer frequencies from a set of DNA sequences to build a feature matrix $X$. You are trying to compute the inverse covariance matrix for a downstream Mahalanobis distance calculation, but the standard matrix $X^T X$ is singular and non-invertible due to highly repetitive and co-occurring sequences in your dataset.

To fix this, you must apply Tikhonov regularization (Ridge penalty) and validate the analytical properties of the resulting smoothed matrix. 

Your tasks are as follows:

1. **Setup the Environment and Data:**
   - Create a Go module named `kmer_extractor` in `/home/user/kmer_app`.
   - Create a FASTA file at `/home/user/sequences.fasta` containing exactly these four sequences:
     ```fasta
     >seq1
     AAAAA
     >seq2
     ACGTG
     >seq3
     AAAAAC
     >seq4
     TTTTT
     ```

2. **Develop the Feature Extractor in Go:**
   - Write a Go program (`/home/user/kmer_app/main.go`) that parses the FASTA file. You must use Go concurrency (e.g., goroutines and channels) to process the sequences in parallel.
   - For each sequence, calculate the exact count of all possible **2-mers** (dinucleotides). There are 16 possible 2-mers, ordered lexicographically: `AA`, `AC`, `AG`, `AT`, `CA`, `CC`, `CG`, `CT`, `GA`, `GC`, `GG`, `GT`, `TA`, `TC`, `TG`, `TT`.
   - Construct the $N \times 16$ feature matrix $X$, where $N$ is the number of sequences (rows) and columns correspond to the 2-mer counts.

3. **Regularization and Analytical Calculation:**
   - Use the `gonum.org/v1/gonum/mat` library to perform matrix operations.
   - Compute the regularized covariance matrix $C = X^T X + \lambda I$, where $\lambda = 0.1$ and $I$ is the $16 \times 16$ identity matrix.
   - Calculate the **trace** (sum of diagonal elements) of the **inverse** of this matrix: $Tr(C^{-1})$.
   - The program should execute and write this final trace value, formatted to exactly four decimal places (e.g., `105.1234`), to `/home/user/trace.txt`.

4. **Scientific Code Regression Testing:**
   - Write a Go test file (`/home/user/kmer_app/main_test.go`) that validates your 2-mer counting logic on the sequence `ACGTG`. The test should fail if the count for `CG` is not exactly 1.
   - Run the tests to ensure they pass.

Run your Go program to generate the target text file.