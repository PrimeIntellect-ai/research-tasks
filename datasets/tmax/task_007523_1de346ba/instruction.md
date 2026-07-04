You are an AI assistant helping a bioinformatics analyst build a custom, reproducible Monte Carlo simulation tool in C++ to establish a null distribution for motif frequencies under random mutation. 

Bioinformatics pipelines often need to determine if a specific DNA motif (like "GATTACA") appears more frequently than expected by chance. We want to simulate a constant mutation rate on a reference sequence and count the expected number of motif occurrences.

Your task is to write a highly reproducible C++ program, create a `Makefile` to build it, and run a computational pipeline to produce the final result.

**Step 1: The C++ Simulation Tool**
Create a C++ program at `/home/user/mc_motif.cpp` that takes exactly 5 command-line arguments:
`./mc_motif <fasta_file> <motif> <mutation_rate_percent> <iterations> <seed>`

*Requirements for `mc_motif.cpp`:*
1. **Fasta Parsing:** Read the input `<fasta_file>`. Ignore lines starting with `>`. Concatenate all other lines (stripping newlines/whitespace) to form the reference DNA sequence. All sequences will be uppercase A, C, G, T.
2. **Monte Carlo Loop:** Run `<iterations>` independent iterations. In each iteration, start with a fresh copy of the reference sequence.
3. **Reproducible Mutation Logic:** To ensure strict cross-platform reproducibility, you **must** use `std::mt19937` and avoid standard library distributions (like `uniform_int_distribution`) which can vary between compilers. Initialize the RNG exactly once before the iteration loop: `std::mt19937 rng(seed);`.
4. **Per-base Mutation:** For *every* character in the sequence (iterating from index 0 to length-1):
   - Draw a random number: `uint32_t r1 = rng();`
   - If `r1 % 100 < mutation_rate_percent`, the base mutates.
   - If it mutates, draw another random number: `uint32_t r2 = rng();`
   - Determine the new base by taking the 3 *other* possible nucleotide bases (from the set A, C, G, T), sorting them alphabetically, and selecting the one at index `r2 % 3`. (For example, if the current base is 'C', the sorted alternatives are 'A', 'G', 'T'. If `r2 % 3 == 1`, the new base becomes 'G').
5. **Motif Counting:** After mutating the sequence for the current iteration, count the number of *overlapping* occurrences of the `<motif>`. (e.g., "AAAA" contains two overlapping "AAA" motifs).
6. **Output:** After all iterations complete, print the average number of motif occurrences per iteration (total motifs counted / number of iterations) formatted to exactly 4 decimal places, followed by a newline.

**Step 2: Build Configuration**
Create a `Makefile` in `/home/user` that compiles `mc_motif.cpp` to an executable named `mc_motif` using `g++` with the `-O3` optimization flag.

**Step 3: Pipeline Execution**
A reference sequence is provided at `/home/user/reference.fasta`. 
Run your pipeline to calculate the expected frequency of the motif `GATTACA` with a mutation rate of `15` percent, over `10000` iterations, using random seed `42`.
Save the standard output of this specific run to `/home/user/result.txt`.