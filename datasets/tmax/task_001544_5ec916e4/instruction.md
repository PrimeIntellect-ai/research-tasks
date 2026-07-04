You are a bioinformatics analyst tasked with analyzing a DNA sequence to identify regions of rapid GC content change. This involves decomposing the sequence into overlapping domains, calculating local properties, and performing numerical differentiation to find the maximum gradient.

The sequence is located at `/home/user/dna_sequence.fasta`.

Your objective is to write and execute a Bash shell workflow (using standard tools like `awk`, `sed`, `grep`, `bash`, etc. - no Python/Perl) to perform the following steps:

1. **Extract and Flatten**: Read the FASTA file, ignore the header line (starts with `>`), and concatenate all sequence lines into a single continuous DNA string.
2. **Domain Decomposition (Sliding Window)**: Divide the sequence into overlapping windows of length `100` bases, with a step size of `50` bases. (Window 0: bases 0-99, Window 1: bases 50-149, Window 2: bases 100-199, etc.).
3. **Local GC Calculation**: For each window, count the total number of 'G' and 'C' characters. This is the GC count for that window.
4. **Numerical Differentiation**: Calculate the absolute difference in GC count between adjacent windows. For example, `Diff[0] = |GC[1] - GC[0]|`, `Diff[1] = |GC[2] - GC[1]|`, and so on.
5. **Find Maximum Gradient**: Identify the 0-based index of the difference array that contains the maximum absolute difference. If there is a tie, select the lowest index.

Finally, write the result to a file at `/home/user/gc_gradient_max.txt` exactly in the following format:
`Index: <idx>, MaxDiff: <val>`
(Replace `<idx>` and `<val>` with your calculated numbers).

Ensure your solution strictly relies on Bash and standard Linux command-line utilities.