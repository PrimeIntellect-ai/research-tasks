You are a bioinformatics analyst working with genomic sequence data. We have a legacy tool, provided as a stripped binary at `/app/seq_domain_splitter`, which performs a 1D "mesh refinement" (domain decomposition) on DNA sequences. 

The binary recursively splits a DNA sequence into smaller domains based on the difference in local probability distributions of nucleotides (A, C, G, T). Because it is a compiled, unmaintained binary, we need you to reverse-engineer it and write a bit-exact equivalent Python script at `/home/user/seq_splitter.py`.

From our internal documentation, we know the algorithm generally behaves as follows:
1. It takes a single DNA sequence (string containing only A, C, G, T) as a command-line argument.
2. It processes the sequence domain `[start, end)`. Initially, `start=0` and `end=len(sequence)`.
3. If the length of the current domain is less than 10 characters, it stops splitting this domain.
4. Otherwise, it calculates the midpoint `mid = start + (end - start) // 2`.
5. It computes the probability distribution (normalized frequency) of single nucleotides (1-mers: A, C, G, T) for the left half `[start, mid)` and the right half `[mid, end)`.
6. It calculates the Manhattan distance (L1 norm) between these two discrete probability distributions.
7. If this distance is strictly greater than a hidden threshold `T`, it splits the domain by recording the `mid` point, and then recursively applies the same procedure to the left half and the right half.
8. The program outputs a comma-separated list of all split boundary indices in ascending order (not including the endpoints `0` and `len(sequence)`). If no splits occur, it outputs an empty string.

Your tasks:
1. Treat `/app/seq_domain_splitter` as a black-box oracle. Use scientific code regression testing practices to experiment with the binary by passing it various crafted DNA strings to deduce the hidden threshold `T`.
2. Implement the equivalent logic in Python 3. The script must be saved at `/home/user/seq_splitter.py` and must accept the sequence as its first command-line argument: `python3 /home/user/seq_splitter.py <sequence>`.
3. The output to `stdout` must be BIT-EXACT identical to the binary's output, including exact formatting (a comma-separated list of integers with no spaces, ending with a newline).

Create `/home/user/regression_log.txt` to log the inputs you used to reverse-engineer the threshold `T`.