You are a bioinformatics analyst tasked with evaluating a newly designed primer's binding affinity across two distinct populations of DNA sequences. 

You need to write a reproducible pipeline in **C** that calculates the optimal alignment score for the primer against each sequence, and then performs a statistical hypothesis test to determine if there is a significant difference in binding affinity between the two populations.

**Setup:**
You have two FASTA files:
1. `/home/user/pop_A.fasta`
2. `/home/user/pop_B.fasta`

The primer sequence to test is: `ATGCGTACG`

**Step 1: Sequence Alignment & Scoring**
Write a C program that reads both FASTA files and calculates the maximum alignment score for the primer against each sequence.
*   **Alignment rule:** The primer must be aligned as a single continuous block without any gaps (a simple sliding window of the primer's length over the sequence).
*   **Scoring function:** For a given window position, the score is `(number of matching bases) - (number of mismatching bases)`. 
*   Find the maximum possible score across all sliding window positions for each sequence.

**Step 2: Statistical Hypothesis Comparison**
Once you have the maximum alignment scores for all sequences in Population A and Population B, compute the following in your C program:
1.  **Mean Score** for Population A ($\bar{X}_A$)
2.  **Mean Score** for Population B ($\bar{X}_B$)
3.  **Welch's t-statistic**, calculated as:
    $t = \frac{\bar{X}_A - \bar{X}_B}{\sqrt{\frac{s_A^2}{N_A} + \frac{s_B^2}{N_B}}}$
    Where $s^2$ is the unbiased sample variance: $s^2 = \frac{1}{N-1} \sum_{i=1}^{N} (X_i - \bar{X})^2$.

**Step 3: Pipeline and Output**
*   Create a `Makefile` in `/home/user` to compile your C code into an executable named `primer_test`.
*   Run your program and output the final results to `/home/user/analysis_result.txt`.
*   The output file must exactly match this format (floating point numbers printed to 4 decimal places):
```
Mean A: [value]
Mean B: [value]
t-statistic: [value]
```

**Constraints:**
*   You must implement the logic in C from scratch (standard C library only).
*   Lines in the FASTA file starting with `>` are sequence identifiers and should be ignored.
*   Sequences in the FASTA files may span multiple lines, but for this task, assume each sequence is provided on a single line immediately following its identifier.