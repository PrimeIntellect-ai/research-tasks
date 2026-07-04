You are an AI assistant helping a data scientist fit a probabilistic model for protein sequences. 

We are comparing empirical amino acid frequencies from a dataset against a known analytical background distribution. We use the Kullback-Leibler (KL) divergence to measure the distance between the empirical distribution ($P$) and the background distribution ($Q$). 

Earlier attempts at calculating this in our Rust pipeline resulted in `NaN` or `Infinity` values due to zero-counts for certain amino acids (analogous to a numerical integrator diverging due to boundary singularities). To fix this, you need to implement a Rust program that applies Laplace (add-one) smoothing.

Your task:
1. Create a new Rust project in `/home/user/bio_divergence`.
2. Write a Rust program that reads a FASTA file located at `/home/user/input.fasta`.
3. Count the occurrences of the 20 standard amino acids across all sequences in the file. The 20 standard amino acids are: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y. Ignore any other characters or gaps.
4. Apply add-one smoothing: add 1 to the count of *each* of the 20 standard amino acids, regardless of whether they appeared in the sequences.
5. Normalize these smoothed counts into a probability distribution ($P$).
6. Read the analytical background distribution ($Q$) from `/home/user/background.csv`. This file has the format `AminoAcid,Probability` (without a header).
7. Calculate the Kullback-Leibler divergence $D_{KL}(P || Q) = \sum P(i) \ln(P(i) / Q(i))$, where $\ln$ is the natural logarithm.
8. Output the final KL divergence value to `/home/user/kl_divergence.txt`, rounded to exactly 4 decimal places (e.g., `0.0152`).

Ensure your Rust code compiles and runs successfully, and writes the correct result to the text file.