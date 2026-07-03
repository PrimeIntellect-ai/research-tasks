You are a bioinformatics analyst working on a novel method to cluster DNA sequences based on their frequency-domain signatures. Your task is to write a high-performance C program that processes DNA sequences, extracts their spectral features, computes their pairwise similarity as probability distributions, and performs matrix decomposition.

The required libraries (`libfftw3-dev` and `liblapacke-dev`) and compilers (`gcc`) are already installed on the system.

Here are the exact requirements:

1. Data Source:
Read a text file located at `/home/user/data/seqs.txt`. This file contains exactly 4 lines. Each line is a DNA sequence of exactly 1024 characters (A, C, G, T).

2. Encoding & Parallel Processing:
Write a C program named `/home/user/analyze_spectra.c`.
Convert each sequence to an array of `double` using the following encoding:
A = 1.0, C = 2.0, G = 3.0, T = 4.0.
Use OpenMP to process the 4 sequences in parallel.

3. Spectral Analysis (FFT):
For each numeric sequence, compute the 1D Real-to-Complex Fast Fourier Transform using FFTW3 (`fftw_plan_dft_r2c_1d`).
Calculate the Power Spectrum for each sequence, which is the squared magnitude of the complex FFT output. (Note: for an input of size 1024, the r2c output has 513 complex elements).

4. Probability Distribution & Similarity Matrix:
Normalize the Power Spectrum of each sequence so that the sum of its elements equals 1.0. Treat these normalized spectra as probability distributions: $P_1, P_2, P_3, P_4$.
Construct a 4x4 similarity matrix $M$ where each element $M_{i,j}$ is the dot product of $P_i$ and $P_j$:
$M_{i,j} = \sum_{k=0}^{512} P_i[k] \times P_j[k]$
To ensure strict positive-definiteness for the next step, add $0.01$ to each diagonal element of $M$.

5. Matrix Decomposition:
Perform a Cholesky decomposition on the matrix $M$ ($M = L L^T$) using LAPACKE (`LAPACKE_dpotrf`, using `LAPACK_ROW_MAJOR`, 'L' for lower).

6. Output:
Extract the 4 diagonal elements of the resulting lower-triangular matrix $L$.
Write these 4 diagonal elements to `/home/user/cholesky_diag.txt`, one per line, formatted to exactly 6 decimal places (`%.6f`).

Once you have written the code, compile it. You should link against OpenMP, FFTW3, LAPACKE, and the math library. Then run your program to produce the output file.