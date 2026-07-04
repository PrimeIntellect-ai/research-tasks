A researcher in our lab is running simulations to calculate DNA substitution probability matrices from sequence alignments. We have a set of observational data in a FASTA file (`/home/user/data/alignment.fasta`) containing two aligned sequences. 

The researcher wrote a C program (`/home/user/sim/sub_matrix.c`) that takes two DNA sequences as command-line arguments, calculates the substitution counts (A, C, G, T), normalizes each row by its sum to get probabilities, and prints the 4x4 matrix.

However, the simulation fails (produces `NaN` values) when the input sequences are missing certain nucleotides. This creates a "near-singular" scenario where a row sum is zero, causing a division by zero during normalization.

Your task is to:
1. Parse the observational data in `/home/user/data/alignment.fasta` to extract the two full, contiguous sequence strings (ignoring the `>` header lines and removing newlines).
2. Diagnose and fix the C program `/home/user/sim/sub_matrix.c`. You must implement Laplace smoothing (add a pseudo-count of `1` to all 16 possible substitution pairs) *before* calculating the row sums and normalizing. This ensures no row sum is zero.
3. Compile your fixed C code.
4. Run the compiled program using the two extracted sequences from the FASTA file as the first and second arguments, respectively.
5. Redirect the standard output of the program to exactly `/home/user/fixed_matrix.txt`.

Ensure your C code maps the nucleotides in the strict alphabetical order: A=0, C=1, G=2, T=3. The output format must be four rows of four space-separated floats with 4 decimal places, as currently formatted in the provided C code.