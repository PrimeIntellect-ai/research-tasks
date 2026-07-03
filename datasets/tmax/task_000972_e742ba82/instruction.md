You are a bioinformatics analyst studying the mutation processes of a specific viral genome. We model the sequence mutations as a Markov chain, where a nucleotide (A, C, G, T) mutates into another nucleotide over a fixed time step.

The transition probability matrix for these mutations has been provided to you in an HDF5 file located at `/home/user/transitions.h5`. The file contains a single dataset named `/matrix` which is a 4x4 matrix of 64-bit floating-point numbers. The rows and columns correspond to the nucleotides A, C, G, and T respectively. Each row sums to 1.0, representing the probability of transitioning from the row's nucleotide to the column's nucleotide.

Your task is to find the stationary distribution of this Markov chain (the steady-state probabilities of finding A, C, G, or T in the long term).

Follow these steps:
1. Extract or inspect the 4x4 matrix from `/home/user/transitions.h5`. You may use standard command-line tools like `h5dump` to read the values.
2. Write a C program at `/home/user/solve_markov.c` that solves for the stationary distribution $\pi$ (such that $\pi P = \pi$, where $P$ is the transition matrix and the sum of $\pi$ is 1.0). You may hardcode the extracted matrix values into your C program to keep the code simple.
3. Compile and execute your C program.
4. Output the resulting stationary distribution into a file named `/home/user/stationary_dist.txt`. 

The output format in `/home/user/stationary_dist.txt` must be a single line containing four comma-separated numbers (for A, C, G, and T), each rounded to exactly 4 decimal places (e.g., `0.2500,0.2500,0.2500,0.2500`). Do not include any trailing spaces or newlines other than the standard POSIX newline at the end.