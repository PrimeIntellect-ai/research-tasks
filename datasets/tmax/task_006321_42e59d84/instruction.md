You are acting as a bioinformatics analyst. We need to statistically compare the sequence lengths between a reference dataset and a newly sequenced query dataset to see if there is a significant difference in their length distributions.

Your task is to write a C program that performs a Monte Carlo permutation test on the sequence lengths extracted from two FASTA files.

Write your C code in `/home/user/compare_fasta_mc.c` and compile it to `/home/user/compare_fasta_mc`.

Here are the requirements for the program:
1. **Parse FASTA Files:** Read `/home/user/ref.fasta` and `/home/user/query.fasta`. Calculate the length of each sequence (ignore the header lines starting with `>`, and do not count newlines in the sequence length).
2. **Observed Statistic:** Calculate the absolute difference in mean sequence lengths between the reference and query datasets: `D_obs = |mean(ref) - mean(query)|`.
3. **Monte Carlo Permutation Test:** 
   - Pool all sequence lengths from both files into a single array (reference lengths first, then query lengths).
   - Perform `100000` (one hundred thousand) permutations of this pooled array.
   - For *each* permutation, use the Fisher-Yates shuffle algorithm. To ensure cross-platform reproducibility, **do not use `rand()`**. Instead, implement and use this exact 32-bit Xorshift PRNG:
     ```c
     #include <stdint.h>
     uint32_t state = 42; // Seed must be 42 exactly
     uint32_t xorshift32() {
         state ^= state << 13;
         state ^= state >> 17;
         state ^= state << 5;
         return state;
     }
     ```
   - For the Fisher-Yates shuffle of an array of size `N`, iterate `i` from `N - 1` down to `1`. In each iteration, pick a random index `j = xorshift32() % (i + 1)`, and swap elements at `i` and `j`.
   - After shuffling, calculate the absolute difference in means between the first `N_ref` elements and the remaining `N_query` elements: `D_perm`.
   - Count how many times `D_perm >= D_obs`.
4. **Calculate and Output:** 
   - The p-value is the count of how many times `D_perm >= D_obs` divided by `100000`.
   - Output the p-value to a file at `/home/user/pvalue.txt` formatted to exactly 4 decimal places (e.g., `0.0451`).

*Note: You do not need to orchestrate a Jupyter notebook for this task, despite the domain primitives; a pure C command-line workflow is expected.*