You are an AI assistant helping a machine learning engineer prepare training data for a biological sequence generation model. The pipeline relies on Non-negative Matrix Factorization (NMF) of sequence k-mer frequency matrices to extract latent features.

However, the current custom C++ NMF implementation crashes (produces NaNs) when the input matrix contains highly similar sequences (near-singular inputs). 

Your tasks are:
1. **Fix the C++ NMF Solver**: Inspect the source code at `/home/user/src/nmf_solver.cpp`. It implements standard Lee and Seung multiplicative update rules. It currently suffers from division-by-zero or near-zero issues. Fix the algorithm by adding a small regularization term (`1e-9`) to the denominators in both the `W` and `H` update rules to prevent NaNs.
2. **Compile the Software**: Compile the fixed C++ code into an executable at `/home/user/nmf_solver` using `g++` with C++11 standard and `-O3` optimization.
3. **Run the Factorization**: Run the solver on the provided near-singular training data.
   Command signature: `./nmf_solver <input_file> <rank> <output_W> <output_H>`
   Input file: `/home/user/data/input_matrix.txt`
   Rank: `5`
   Output files: `/home/user/W.txt` and `/home/user/H.txt`
4. **Calculate Distribution Distance Metric**: The engineer needs to know the approximation quality. Write a Python script at `/home/user/evaluate.py` that:
   - Reads the original matrix `V` (`input_matrix.txt`), and the outputs `W` and `H`.
   - Reconstructs the approximated matrix `V_approx = W @ H`.
   - Flattens both `V` and `V_approx` into 1D arrays and normalizes them so they sum to 1.0 (treating them as probability distributions).
   - Calculates the Kullback-Leibler (KL) divergence from `V_approx` (Q) to `V` (P), i.e., `KL(P || Q) = sum(P * log(P / Q))`.
   - Writes the resulting KL divergence as a single floating-point number to `/home/user/kl_divergence.txt`.

Ensure your C++ fix is correct, the compilation succeeds, and the evaluation script generates the required metric file.