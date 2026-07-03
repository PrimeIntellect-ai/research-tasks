You are a bioinformatics analyst tasked with analyzing a set of DNA sequences using k-mer frequency matrices, matrix decompositions, and linear modeling. 

You have been provided a FASTA file containing several DNA sequences at `/home/user/data/seqs.fasta`.

Your goal is to write a Python script `/home/user/analyze_kmers.py` that performs the following steps:
1. **K-mer Matrix Construction**: Read the FASTA file. For each sequence (in the exact order they appear in the file), count the frequencies of all possible overlapping 3-mers (there are $4^3 = 64$ possible 3-mers: AAA, AAC, AAG, AAT, CAA, etc.). Construct an $N \times 64$ matrix $A$, where $N$ is the number of sequences, and columns represent the 64 3-mers sorted in strict alphabetical order.
2. **Matrix Decomposition**: Compute the Singular Value Decomposition (SVD) of $A$. Extract the top 3 singular values. Save these 3 values (comma-separated, rounded to 4 decimal places) to `/home/user/svd_out.txt`.
3. **Linear Equation Solving**: We want to predict the GC-content (total number of 'G' and 'C' characters in a sequence) based on the 3-mer profile using Ridge Regression. Let $Y$ be a column vector of length $N$ where $Y_i$ is the total count of 'G' and 'C' nucleotides in the $i$-th sequence. Solve the linear system $(A^T A + \lambda I) w = A^T Y$ for the weight vector $w$, where $\lambda = 1.0$ and $I$ is the $64 \times 64$ identity matrix.
4. **Output**: Calculate the sum of all elements in the vector $w$. Save this sum (rounded to 4 decimal places) to `/home/user/w_sum.txt`.

Ensure your script is self-contained and handles the math efficiently using `numpy` and `scipy`. Run your script to generate the required output files.

Note: Only standard ACGT characters are present in the sequences. Overlapping 3-mers means the sequence "ACGTA" contains "ACG", "CGT", and "GTA".