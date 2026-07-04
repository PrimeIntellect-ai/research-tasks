You are an AI assistant helping a bioinformatics analyst process nucleotide transition data. 

We are modeling DNA sequences as a Markov chain with 4 states: A, C, G, and T. You have been provided with a dataset of observed adjacent nucleotide transitions in `/home/user/transitions.csv`. Each line contains a pair of nucleotides (e.g., `A,C` meaning A is followed by C).

Your task is to estimate the 95% bootstrap confidence interval for the steady-state probability of Adenine ('A') in this Markov model. 

You must write a Rust program in `/home/user/markov_ci` to do the following:
1. Initialize a Cargo project and add dependencies: `rayon`, `rand` (use version 0.8), and `nalgebra`.
2. Read the pairs from `/home/user/transitions.csv`.
3. Perform 1000 bootstrap iterations in parallel using `rayon`.
    * For each iteration, you must use a seeded PRNG (`rand::rngs::StdRng::seed_from_u64(iteration_index as u64)`) to sample `N` transitions with replacement, where `N` is the total number of transitions in the original file. Use `rand::seq::SliceRandom::choose` to sample the lines.
    * Build the $4 \times 4$ transition probability matrix $P$ for the states [A, C, G, T] from the bootstrapped sample. Ensure each row sums to 1.
    * Solve the linear system to find the steady-state distribution $\pi$ (such that $\pi P = \pi$ and $\sum \pi_i = 1$). Use `nalgebra` to solve this linear system.
    * Record the steady-state probability of 'A'.
4. Sort the 1000 steady-state probabilities for 'A' and determine the 95% confidence interval using the 2.5th and 97.5th percentiles (indices 25 and 975 in the sorted array).
5. Output the result to a file `/home/user/result.txt` in exactly this format:
   `CI for A: [0.1234, 0.5678]` (round to 4 decimal places).

Compile and run your Rust program to generate the output file.