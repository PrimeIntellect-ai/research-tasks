Act as a Machine Learning Engineer preparing biological sequence data for a clustering model. You need to write a Rust program that parses raw DNA reads, identifies sequences with a specific primer, reshapes the data into k-mer frequency distributions, and safely calculates a numerically stable distance matrix.

Your task is to create a Rust project in `/home/user/kmer_kl` and write an executable that performs the following steps:

1. **Read the raw data:** Parse the FASTA file located at `/home/user/reads.fasta`.
2. **Primer Alignment & Truncation:** For each sequence, find the *first* occurrence (from the left) of the primer sequence `ATGCGTAC`, allowing for **at most 1 character substitution mismatch** (insertions and deletions are not allowed). 
   - If the primer is found, extract the substring immediately following the matched primer to the end of the sequence.
   - If the primer is not found, discard the read entirely.
3. **Select subset:** Take the *first 4* successfully truncated substrings (in the order they appeared in the FASTA file).
4. **Data Reshaping (k-mer extraction):** For each of the 4 substrings, convert it into a 3-mer (k=3) frequency distribution. There are 64 possible 3-mers using the alphabet `A, C, G, T`. 
5. **Numerical Stability:** Because some 3-mers will have a count of 0, applying a log function later would cause numerical instability (`-inf`). Add a pseudo-count of `1e-8` to the count of *all 64 possible 3-mers* for each sequence *before* calculating the probabilities. Normalize the counts so that the 64 probabilities sum to 1.0 for each sequence.
6. **Distance Calculation:** Calculate the pairwise Kullback-Leibler divergence matrix $D_{KL}(P || Q)$ between the 4 sequences.
   - Use the natural logarithm ($\ln$).
   - $D_{KL}(P || Q) = \sum_{i=1}^{64} P(i) \ln\left(\frac{P(i)}{Q(i)}\right)$
7. **Output:** Write the resulting 4x4 distance matrix to `/home/user/features.json`. The file should contain a JSON array of arrays (e.g., `[[0.0, ...], ...]`), where every float is rounded to exactly 4 decimal places.

To complete this task, you must rely on standard Rust tools (you can use `cargo` and public crates like `serde_json`). Do not use any external scripts to bypass writing the Rust logic. Run your Rust code so that `/home/user/features.json` is generated successfully.