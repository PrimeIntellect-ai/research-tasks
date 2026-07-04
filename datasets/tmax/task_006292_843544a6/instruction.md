You are a bioinformatics analyst working with bash command-line tools. You have been given two files in your home directory `/home/user/`:
1. `reads.tsv`: A tab-separated file containing sequencing read data. The columns are `SampleID`, `ReadID`, and `Sequence`. There are exactly two samples in this file: `SampleA` and `SampleB`.
2. `reference.fasta`: A standard FASTA file containing a single continuous reference sequence (the first line starts with `>` and the subsequent lines contain the sequence, which may be wrapped).

Your task is to build a reproducible computation pipeline using pure bash and standard Linux text processing tools (like `awk`, `grep`, `sed`, `tr`) to perform two specific analyses:

**Analysis 1: Probability Distribution Distance**
1. Extract the sequence length of every read in `reads.tsv`.
2. Compute the empirical probability distribution of sequence lengths for `SampleA` and `SampleB` separately. (The probability of length *L* in a sample is the number of reads of length *L* divided by the total number of reads in that sample).
3. Calculate the Total Variation Distance (TVD) between the length distributions of `SampleA` and `SampleB`. 
   *Note: TVD is defined as `0.5 * sum(|P_A(L) - P_B(L)|)` across all observed lengths L.*
4. Save the calculated TVD, formatted to exactly 4 decimal places, to a file named `/home/user/tvd_result.txt`.

**Analysis 2: Sequence Domain Decomposition & GC Content**
1. Extract the raw sequence from `/home/user/reference.fasta` (ignoring the `>` header line and removing any newlines so it is one continuous string).
2. Decompose (chunk) this continuous sequence into contiguous, non-overlapping windows (bins) of exactly 50 base pairs (bp) each. Discard any remaining base pairs at the end that are less than 50 bp.
3. For each 50-bp bin, calculate the GC content percentage (the number of 'G' and 'C' characters divided by 50, multiplied by 100).
4. Identify the 1-based indices of the bins (Bin 1 is the first 50 bp, Bin 2 is the next 50 bp, etc.) that have a GC content strictly greater than or equal to 60.0%.
5. Write the indices of these high-GC bins, one per line, sorted in ascending order, to a file named `/home/user/high_gc_bins.txt`.

Ensure your solutions are robust and rely only on standard CLI tools available in bash. Do not write python or perl scripts.