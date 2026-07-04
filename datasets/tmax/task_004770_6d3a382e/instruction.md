You are a bioinformatics analyst tasked with preprocessing genomic sequences for a downstream Genome-Wide Association Study (GWAS) pipeline. Our pipeline is notoriously fragile and crashes when fed sequences that yield near-singular k-mer transition matrices (typically low-complexity or highly repetitive regions).

Your objective is two-fold:

**Part 1: Fix the Vendored SVD Library**
We use a specialized internal C library called `libkmer-svd` (version 1.2.0) to compute condition numbers of sequence transition matrices. 
The source code has been vendored at `/app/libkmer-svd-1.2.0/`. However, the current build configuration has a deliberate perturbation: the `Makefile` is broken. It fails to compile the shared library properly because it is missing the position-independent code flag (`-fPIC`) for its object files, and it omits the math library (`-lm`) during linking, which causes the downstream tools to fail.
1. Fix the `Makefile` in `/app/libkmer-svd-1.2.0/`.
2. Compile the library (`make`) and install it so it can be linked by your code. The known-good code path we will test is the `kmer_matrix_condition_number(double* matrix, int n)` function exported by the library.

**Part 2: Implement the Sequence Filter**
You must write a C program located at `/home/user/seq_filter.c` (and compile it to `/home/user/seq_filter`). This executable must act as a filter/classifier for `.fasta` sequence files.

It must take a single command-line argument (the path to a `.fasta` file) and print exactly `ACCEPT` or `REJECT` to standard output.

The filtering logic must be:
1. **Observational Data Reshaping**: Read the first DNA sequence from the provided `.fasta` file (ignore the header starting with `>`). Convert the sequence into a binary signal array of length $N$ (where $N$ is the sequence length), where 'G' or 'C' = 1.0, and 'A' or 'T' = 0.0.
2. **Spectral Analysis**: Compute the 1D Discrete Fourier Transform (DFT) magnitude (power spectrum) of this binary signal. You may use a simple O(N^2) DFT implementation or link against FFTW3 if you prefer. Calculate the ratio of "high-frequency power" (sum of magnitudes for frequencies $k > N/4$) to the total power (sum of all magnitudes).
3. **Linear Equation / SVD Check**: Use the fixed `libkmer-svd` library to compute the condition number of the sequence's 4x4 dinucleotide transition matrix (frequencies of AA, AC, AG, AT, CA, etc., normalized such that each row sums to 1.0). 
4. **Decision**: `REJECT` the sequence if the high-frequency power ratio is less than `0.10` OR if the condition number of the transition matrix is greater than `1000.0` (indicating near-singularity). Otherwise, `ACCEPT`.

**Corpora for Verification**
You must ensure your program works perfectly against our test corpora:
- Clean sequences (should be ACCEPTED): `/home/user/data/clean/`
- Evil sequences (should be REJECTED): `/home/user/data/evil/`

Your final deliverable is the compiled binary `/home/user/seq_filter` and the fixed library in `/app/libkmer-svd-1.2.0/`.