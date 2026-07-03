You are a bioinformatics analyst restricted to a purely Bash-based toolchain (no Python, R, or Perl). You have been given a FASTA file containing DNA sequences. You must extract basic sequence metrics, perform a linear regression, and estimate the density distribution of the data.

Your input file is located at `/home/user/sequences.fasta`.

Perform the following tasks using only Bash, awk, sed, coreutils, or bc:

1. **Calculate GC Content and Length**
   Parse `/home/user/sequences.fasta`. For each sequence, calculate its length and its GC content percentage (Number of G and C / Total length * 100).
   Note: Sequences may span multiple lines. Only count A, C, G, T characters.
   Save the results in `/home/user/gc_content.tsv` in the format:
   `sequence_id \t length \t gc_content`
   (Do not include the `>` character in the sequence_id. Output the GC content formatted to exactly 4 decimal places).

2. **Linear Regression**
   Perform a simple linear regression using Ordinary Least Squares (OLS) where the independent variable (X) is the sequence `length` and the dependent variable (Y) is the `gc_content`.
   Calculate the slope (m) and the intercept (b).
   Save the results in `/home/user/regression.log` with the format:
   `slope intercept`
   (Format both values to exactly 4 decimal places, separated by a space).

3. **Density Estimation (Histogram)**
   Create a histogram of the GC content values using bin sizes of 10. The bins should be [0,10), [10,20), ..., [90,100]. Note that the last bin should be inclusive of 100 if any sequence has 100% GC.
   Count the number of sequences that fall into each bin.
   Save the results in `/home/user/histogram.log` in the format:
   `bin_start count`
   (Include all bins from 0 to 90, even if the count is 0. Ensure bins are sorted in ascending order).