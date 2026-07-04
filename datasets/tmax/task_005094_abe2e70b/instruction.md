You are a bioinformatics analyst building a reproducible, open-source pipeline for a proprietary nanopore sequencing device. The vendor has provided a closed-source, stripped binary located at `/app/nanopore_scorer` which calculates a signal match score between a candidate DNA primer sequence and a raw spectroscopic signal read.

Your goal is to reverse-engineer the signal processing and alignment logic of this proprietary binary and write a bit-exact C equivalent. 

The binary `/app/nanopore_scorer` operates as follows:
- It takes command line arguments: first, a DNA sequence string (containing A, C, G, T), followed by $N$ floating-point numbers representing the raw signal data, where $N$ is the length of the sequence.
- Example invocation: `/app/nanopore_scorer ACGT 1.05 -0.95 0.55 -0.42`
- It applies a causal digital filter (a basic smoothing operation) to the raw signal.
- It maps the DNA string to expected theoretical signal levels.
- It computes a single floating point score representing the distance (e.g., Euclidean or sum-of-absolute-differences) between the filtered signal and the expected signal.
- It prints the resulting float to standard output formatted to exactly 4 decimal places (e.g., `1.2345`).

Your Tasks:
1. Probe `/app/nanopore_scorer` with various sequences and signal values to deduce:
   - The theoretical signal levels for A, C, G, and T.
   - The exact coefficients of the causal signal filter (it relies on current and past samples).
   - The exact distance metric used.
2. Write a clean, well-commented C implementation of this algorithm in `/home/user/open_scorer.c`.
3. Compile your program to `/home/user/open_scorer` using `gcc -O2 -o /home/user/open_scorer /home/user/open_scorer.c -lm`.

The automated verifier will randomly fuzz both your `/home/user/open_scorer` and `/app/nanopore_scorer` with thousands of valid sequences and signal arrays to ensure bit-exact output equivalence.