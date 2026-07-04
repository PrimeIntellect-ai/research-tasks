You are a bioinformatics analyst processing DNA sequences to find underlying patterns in short sequence motifs. 

Your task is to build a Rust-based tool that calculates the overlapping 3-mer (trinucleotide) frequency matrix for a set of DNA sequences and performs Singular Value Decomposition (SVD) to extract the principal components.

Here are the requirements:
1. You have a FASTA file located at `/home/user/data/seqs.fasta`.
2. Initialize a new Rust executable project in `/home/user/bio_svd`.
3. Write a Rust program that:
   - Reads the sequences from the FASTA file. Ignore the header lines (those starting with `>`). You can assume each sequence spans exactly one line following its header.
   - For each sequence, count the occurrences of all possible overlapping 3-mers (e.g., "AAA", "AAC", ... "TTT").
   - Construct an N x 64 matrix of type `f64` (where N is the number of sequences). Each row represents a sequence, and each column represents a 3-mer count.
   - The columns MUST be ordered alphabetically by the 3-mer string (i.e., column 0 is "AAA", column 1 is "AAC", ..., column 63 is "TTT").
   - Perform an SVD on this matrix. You should use the `nalgebra` crate for matrix decomposition.
   - Extract the singular values of the matrix.
   - Write the top 3 largest singular values to `/home/user/svd_results.txt`. Each value should be on a new line, formatted to exactly 4 decimal places.

To complete the task, run your Rust program so that `/home/user/svd_results.txt` is generated with the correct values.