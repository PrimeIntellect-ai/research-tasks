As a performance engineer, you are profiling a legacy spectroscopy analysis pipeline. The bottleneck is a closed-source, single-threaded binary located at `/app/spec_oracle` (which has been stripped of symbols). 

This oracle reads a collection of spectra and computes a pairwise distance matrix between all spectra. Each spectrum is represented as a sequence of signal intensities over $M$ discrete bins, pre-normalized so that the intensities in each spectrum sum to $1.0$ (acting as a 1D probability distribution). 

Your task is to:
1. Reverse-engineer / infer the exact distance metric the oracle computes. You can do this by creating small test inputs, running `/app/spec_oracle <input> <output>`, and analyzing the outputs. (Hint: It is a standard probability distribution distance metric commonly used in optimal transport for 1D discrete distributions).
2. Write a highly optimized, OpenMP-parallelized C program `fast_spec.c` that computes this exact same distance matrix.
3. Compile your program to `/home/user/fast_spec` using `gcc -O3 -fopenmp fast_spec.c -o /home/user/fast_spec -lm`.

**Input Format:**
The first line contains two integers $N$ (number of spectra) and $M$ (number of bins).
The next $N$ lines each contain $M$ space-separated floats representing the spectrum.

**Output Format:**
A text file with $N$ lines, each containing $N$ space-separated floats formatted to at least 6 decimal places, representing the symmetric pairwise distance matrix.

Your binary must be executable as: `/home/user/fast_spec input_data.txt output_matrix.txt`

The automated test will evaluate your compiled `/home/user/fast_spec` on a large hidden dataset. It will measure the Mean Squared Error (MSE) of your output compared to the oracle, and also measure execution time. You must achieve an MSE $< 10^{-8}$.