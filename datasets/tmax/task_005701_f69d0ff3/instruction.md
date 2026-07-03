You are a performance engineer working on a bioinformatics pipeline. A legacy sequence alignment and primer design tool is crashing because its probability distribution distance calculations fail (producing `NaN` or panicking) on near-singular inputs—specifically, when comparing sequences that lack certain k-mers, leading to division-by-zero errors in Kullback-Leibler (KL) divergence.

Your task is to implement a robust Rust utility that calculates the Jensen-Shannon Divergence (JSD) between the 3-mer (trimer) frequency distributions of two candidate primer sequences. JSD is symmetric and handles zero-frequencies better, but to completely avoid near-singular density estimation issues, you must also apply Laplace smoothing.

You will find the input file at `/home/user/primers.fa`. It contains exactly two DNA sequences (one per line, ignoring any lines starting with `>`).

Write and execute a Rust program that does the following:
1. Parses the two DNA sequences from `/home/user/primers.fa`.
2. Computes the 3-mer frequency count for both sequences. There are $4^3 = 64$ possible 3-mers using the alphabet {A, C, G, T}. Overlapping 3-mers should be counted (e.g., `ATGC` contains `ATG` and `TGC`).
3. Applies Laplace smoothing with a pseudocount of `1` to all 64 possible 3-mers for both sequences. (i.e., add 1 to the count of every possible 3-mer, even if it doesn't appear in the sequence).
4. Converts these smoothed counts into probability distributions $P$ and $Q$ (ensure they sum to 1.0).
5. Calculates the Jensen-Shannon Divergence between $P$ and $Q$.
   The formula is: $JSD(P \parallel Q) = \frac{1}{2} D_{KL}(P \parallel M) + \frac{1}{2} D_{KL}(Q \parallel M)$
   Where $M = \frac{1}{2}(P + Q)$, and $D_{KL}(X \parallel Y) = \sum_{i} X_i \ln\left(\frac{X_i}{Y_i}\right)$ (use the natural logarithm).
6. Writes the final JSD value, formatted to exactly 6 decimal places (e.g., `0.012345`), to a file at `/home/user/jsd_result.txt`.

You may create your Rust project anywhere in `/home/user/`, such as `/home/user/jsd_calc`. You only need the standard Rust library. Ensure your program compiles and runs successfully, and creates the expected output file.