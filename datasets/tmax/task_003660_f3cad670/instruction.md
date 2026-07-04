You are a bioinformatics analyst tasked with developing a Go tool to detect hidden periodicities in DNA sequences using Fourier analysis and statistical hypothesis testing. Repetitive motifs often indicate structural or regulatory functions.

Your task is to write a Go program that analyzes DNA sequences, computes their frequency spectrum, and tests the hypothesis that the sequence contains a statistically significant periodic signal against a null hypothesis of random noise.

Perform the following steps:

1. Environment Setup:
   - Create a directory `/home/user/dnastat` and initialize a Go module named `dnastat`.
   - You may use the `github.com/mjibson/go-dsp/fft` package for Fourier transforms, or any standard math library.

2. Code Implementation (`/home/user/dnastat/analyzer.go`):
   - Write a Go program that takes a single file path as a command-line argument. The file contains a single DNA string (A, C, G, T) on one line.
   - Convert the DNA sequence to a sequence of real numbers using the following encoding:
     `A = 1.0`, `C = -1.0`, `G = 2.0`, `T = -2.0`.
   - Pad the numeric sequence with `0.0` at the end until its length is exactly the next power of 2 (e.g., if length is 10, pad to 16).
   - Compute the Fast Fourier Transform (FFT) of this real sequence.
   - Compute the Power Spectrum for each frequency bin: `Power = Real^2 + Imag^2`.
   - Exclude the DC component (index 0) from the following statistical analysis.
   - Calculate the mean and standard deviation of the remaining power values.
   - Find the maximum power value (excluding DC) and calculate its Z-score: `Z = (MaxPower - MeanPower) / StdDev`.
   - Determine the hypothesis: If `Z >= 3.00`, the hypothesis is `Periodic`; otherwise, it is `Random`.
   - The program should print exactly one line to standard output in the following format:
     `File: <basename>, Z: <z_score>, Hypothesis: <Periodic/Random>`
     (Format the Z-score to exactly 2 decimal places, e.g., `Z: 4.12`).

3. Regression Testing & Execution:
   - I have placed two sequence files in `/home/user/data/`: `seq1.txt` and `seq2.txt`.
   - Write a bash script `/home/user/dnastat/run_analysis.sh` that builds your Go program and runs it on both `seq1.txt` and `seq2.txt` (in that order).
   - The script should redirect the output of both runs into `/home/user/dnastat/results.log`.

Constraints:
- Run the bash script to generate the final `results.log`.
- Ensure your math for the sample standard deviation uses `N` (population std dev) or `N-1` (sample std dev) - use `N` (population) for this task: `sqrt( sum((x - mean)^2) / N )`.