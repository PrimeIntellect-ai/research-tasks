You are an AI assistant helping a bioinformatics researcher analyze the thermodynamic stability of a DNA sequence and compile a custom statistical tool.

Your goal is to complete a multi-phase task involving bioinformatics parsing, numerical integration/differentiation, and C compilation.

**Phase 1: Python Analysis Script**
Write a Python script at `/home/user/analyze.py` that does the following:
1. Parses the FASTA file located at `/home/user/data/target.fasta`. This file contains a single DNA sequence. Do not use external bioinformatics libraries (like Biopython) for parsing; just use standard Python.
2. Calculates the running GC count for a sliding window of size $W=10$. Let $C[i]$ be the number of 'G' or 'C' characters in the substring from index $i$ to $i+9$ (inclusive). For a sequence of length $L$, there will be $L-9$ such windows.
3. Computes the numerical derivative $D[i] = C[i] - C[i-1]$ for $1 \le i \le L-10$.
4. Computes the numerical integral of $D[i]^2$ over the indices using the trapezoidal rule (you may use `numpy.trapz`).
5. Writes the final integral value (formatted to exactly two decimal places, e.g., `9.50`) to the first line of the file `/home/user/result.txt`.

**Phase 2: Compilation and Execution Pipeline**
There is a C source file located at `/home/user/src/fasta_stat.c` which contains a program that counts the number of sequences in a FASTA file.
Write a bash script at `/home/user/run_all.sh` that automates the entire pipeline:
1. Compiles the C program into an executable at `/home/user/fasta_stat` using `gcc`.
2. Runs your Python script `/home/user/analyze.py` to generate the initial `/home/user/result.txt`.
3. Runs the compiled `/home/user/fasta_stat` executable, passing `/home/user/data/target.fasta` as the argument.
4. Appends the standard output of the C program to `/home/user/result.txt`.

**Execution:**
Once you have created both `/home/user/analyze.py` and `/home/user/run_all.sh`, run `/home/user/run_all.sh` so that `/home/user/result.txt` is populated with the correct answers. Make sure `run_all.sh` has executable permissions.