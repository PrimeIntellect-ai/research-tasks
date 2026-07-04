You are a bioinformatics analyst tasked with identifying protein-coding regions using spectral analysis. It is known that protein-coding DNA sequences often exhibit a period-3 periodicity (a frequency of 1/3) due to codon usage bias. 

To use standard signal processing (FFT) on DNA, we must map the characters (A, C, G, T) to numerical values. Your goal is to find the *optimal* numerical mapping that maximizes this period-3 signal for a known coding sequence, and then apply this mapping to rank a set of unknown sequences.

Here are your instructions:

1. **Environment Setup:** 
   Create a Python virtual environment at `/home/user/bio_env`. Install `numpy`, `scipy`, and `biopython`.

2. **Data:**
   You have been provided with a FASTA file at `/home/user/data/sequences.fasta`. The sequence labeled `seq_train` is a known coding sequence.

3. **Optimization:**
   Write a Python script to find the optimal weights ($w_A, w_C, w_G, w_T$) that maximize the relative period-3 power of `seq_train`.
   - **Signal Generation:** Convert the sequence of length $N$ into a numerical array $x$ where each base is replaced by its corresponding weight.
   - **Normalization:** Inside your objective function, before evaluating the signal, normalize the weights vector $w = [w_A, w_C, w_G, w_T]$ such that its Euclidean norm is 1 ($||w||_2 = 1$). 
   - **FFT:** Compute the discrete Fourier transform $X$ of the signal $x$. Let the power spectrum be $P = |X|^2$.
   - **Relative Power:** The target frequency index is exactly $k = N / 3$ (assume $N$ is a multiple of 3). The relative period-3 power is defined as $R = P_k / \sum_{i=0}^{N-1} P_i$.
   - **Objective:** Use `scipy.optimize.minimize` (e.g., Nelder-Mead) to minimize $-R$. 
   - **Initial Guess:** Start with the guess $w = [1.0, 0.5, -0.5, -1.0]$ for [A, C, G, T] respectively.

4. **Ranking:**
   Once you have the optimized (and normalized) weights, calculate the relative period-3 power $R$ for *all* sequences in the FASTA file (including `seq_train`).

5. **Output:**
   Create a JSON file at `/home/user/results.json` containing the exact keys below:
   - `"optimal_weights"`: A dictionary `{"A": wa, "C": wc, "G": wg, "T": wt}` representing the final normalized optimal weights.
   - `"seq_train_power"`: The maximum relative period-3 power $R$ achieved for `seq_train` (as a float).
   - `"ranking"`: A list of sequence IDs sorted in descending order of their relative period-3 power.

Make sure your code strictly follows the mathematical definitions provided.