You are a bioinformatics analyst tasked with analyzing DNA sequences using k-mer frequencies and dimensionality reduction.

I have a file at `/home/user/sequences.fasta` containing 500 DNA sequences. I need you to perform the following steps to analyze their 3-mer distributions:

1. Write a Python script (you can name it `/home/user/analyze.py`) that parses the FASTA file.
2. For each sequence, calculate the frequencies of all overlapping 3-mers (there are 64 possible 3-mers from AAA to TTT).
3. Reshape this observational data into a feature matrix $M$ of size $N \times 64$ (where $N$ is the number of sequences). The columns must correspond to the 64 3-mers sorted in standard alphabetical order (AAA, AAC, AAG, AAT, CAA, etc.).
4. Center the matrix by subtracting the mean of each column from that column.
5. Perform Singular Value Decomposition (SVD) on this centered matrix to extract the principal components.
6. Write the top 2 singular values (the two largest ones) to `/home/user/top_singular_values.txt`, one per line, rounded to 4 decimal places.
7. To validate the matrix decomposition, calculate the Frobenius norm of the full centered matrix $M$, and the Frobenius norm of the rank-2 approximated matrix (using only the top 2 singular components). Save these two values (full norm, rank-2 norm), rounded to 4 decimal places, separated by a comma, on a single line to `/home/user/norms.txt`.

Ensure your environment has the necessary packages installed (e.g., `numpy`, `biopython` if needed). Execute your script to produce the required output files.