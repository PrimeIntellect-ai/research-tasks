You are a performance engineer working on a bioinformatics pipeline that processes large volumes of genomic data. The pipeline relies on a proprietary local package called `py_kmer_counter` for fast k-mer extraction, but the package currently fails to install due to a packaging perturbation made by a previous developer.

Your task consists of two parts:

1. **Fix and Install the Vendored Package:**
   - The source code for `py_kmer_counter` version 1.0 is located at `/app/py_kmer_counter-1.0`.
   - Identify and fix the error in its installation script so that it can be installed correctly.
   - Install the package into your system's Python environment. The package provides a function `py_kmer_counter.count_3mers(sequence)` which returns a dictionary of 3-mer counts.

2. **Implement the Analysis Script:**
   - Write a Python script at `/home/user/solve.py`.
   - The script must read a single DNA sequence (a string of A, C, G, T) from standard input (`sys.stdin`).
   - Use the `py_kmer_counter` package to get the counts of all 64 possible 3-mers (from "AAA" to "TTT" in lexicographical order).
   - Form an 8x8 matrix from these 64 counts in row-major order (i.e., the first row contains counts for "AAA", "AAC", "AAG", "AAT", "ACA", "ACC", "ACG", "ACT", and so on).
   - Perform Singular Value Decomposition (SVD) on this 8x8 matrix using `numpy`.
   - Print *only* the largest singular value to standard output, formatted to exactly 4 decimal places (e.g., `12.3456`).

Your implementation in `/home/user/solve.py` will be extensively fuzzed with random DNA sequences and tested for strict bit-exact equivalence against an oracle implementation. Make sure your matrix construction strictly follows the lexicographical ordering of 3-mers.