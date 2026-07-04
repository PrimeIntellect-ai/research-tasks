You are a bioinformatics analyst tasked with evaluating the compositional variance of a set of DNA sequences. 

Your objective is to extract nucleotide frequency features from a FASTA file, reshape these observations into a numerical matrix, and perform a Singular Value Decomposition (SVD) to find the primary axis of variance.

Please complete the following steps:
1. Initialize a new Rust binary project named `freq_svd` in `/home/user/freq_svd`.
2. Add the `nalgebra` crate as a dependency in your `Cargo.toml` to handle matrix operations.
3. Write a Rust program in `/home/user/freq_svd/src/main.rs` that reads a FASTA file located at `/home/user/data/sequences.fasta`.
4. Parse the FASTA file. For each sequence (ignoring the header lines starting with `>`), count the total occurrences of the nucleotides 'A', 'C', 'G', and 'T' (case-insensitive). Ignore any other characters.
5. Reshape this observational data into an $N \times 4$ matrix of 64-bit floats (`f64`), where $N$ is the number of sequences. The columns must strictly correspond to the counts of 'A', 'C', 'G', and 'T' in alphabetical order. Row 0 should correspond to the first sequence in the file, Row 1 to the second, and so on.
6. Use `nalgebra` to compute the Singular Value Decomposition (SVD) of this matrix and extract the largest singular value. This validates the principal analytical component of the sequence compositions.
7. Write ONLY the largest singular value, formatted to exactly 3 decimal places (e.g., `12.345`), to a file at `/home/user/output.txt`.
8. Compile and run your project to produce the output file.

Do not write any extra text in `/home/user/output.txt` other than the rounded float value. Ensure all file paths match exactly as requested.