You are a bioinformatics analyst assisting with a mathematical modeling project. We are trying to predict the binding affinity of various DNA sequences based on their k-mer profiles. 

We have a dataset of sequences and their corresponding continuous affinity scores in `/home/user/binding_data.txt`. Each line is formatted as `sequence,score`.

The sequences were generated using a specific forward primer: `ATGCGATCG`. 
However, the data is noisy, and our current Ordinary Least Squares (OLS) script fails. The k-mer frequency matrix is highly collinear (and contains all-zero columns for 3-mers that never appear), making the covariance matrix $X^T X$ near-singular. As a result, standard matrix inversion yields garbage or NaN values.

Your task is to write a C++ program that performs the following steps:
1. **Data Reshaping & Primer Alignment:** Read `/home/user/binding_data.txt`. For each line, verify if the sequence starts exactly with the primer `ATGCGATCG`. If it does NOT, discard the record. If it does, trim the primer from the sequence.
2. **K-mer Extraction:** For the trimmed sequence, compute the frequency (count) of all possible 3-mers (substrings of length 3). There are $4^3 = 64$ possible 3-mers. 
3. **Matrix Construction:** Construct a feature matrix $X$ (N rows by 64 columns), where columns are ordered alphabetically by the 3-mer string (i.e., AAA, AAC, AAG, AAT, ACA, ..., TTT). Construct a target vector $y$ (N rows) from the affinity scores.
4. **Regularized Factorization:** To handle the near-singular matrix, compute the Ridge Regression (Tikhonov regularization) weights instead of OLS. The weight vector $w$ is given by:
   $w = (X^T X + \lambda I)^{-1} X^T y$
   Use a regularization parameter of $\lambda = 2.0$.
5. **Output Generation:** Save the computed 64-dimensional weight vector to `/home/user/kmer_weights.csv`. 
   - The file must contain exactly 64 lines.
   - Each line should be formatted as: `3-mer,weight` (e.g., `AAA,0.1234`).
   - Round the weights to 4 decimal places.

**Environment Details:**
- You should use C++ to solve this problem.
- The Eigen3 library is installed on the system (headers are at `/usr/include/eigen3`). You can compile your code with `g++ -O3 -I/usr/include/eigen3 solution.cpp -o solution`.
- There is no boilerplate code; you must write the C++ code from scratch.