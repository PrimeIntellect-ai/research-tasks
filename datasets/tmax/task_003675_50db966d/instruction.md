You are acting as a bioinformatics analyst. We need to compare the read length distributions of two different Nanopore sequencing runs to identify potential biases in the sequencing pores.

Your task consists of the following steps:

1. **Compile the Length Extractor**: 
   In `/home/user/src/`, you will find a C source file named `extractor.c`. This is a custom, highly optimized sequence length extractor written for our proprietary fasta-like format. Compile this C code into an executable named `extractor` in the same directory using `gcc`.

2. **Process the Sequences**:
   In `/home/user/data/`, there are two sequence files: `run_A.fasta` and `run_B.fasta`. 
   Use the compiled `extractor` tool to extract the sequence lengths from both files. The tool reads a file from standard input and prints the length of each sequence to standard output, one per line. (e.g., `./extractor < ../data/run_A.fasta > lengths_A.txt`).

3. **Density Estimation and Distance Calculation**:
   Write a Python script (e.g., `/home/user/analyze.py`) to perform the following analysis on the extracted lengths:
   - Load the lengths for run A and run B.
   - Fit a Gaussian Kernel Density Estimate (KDE) to each set of lengths. Use `scipy.stats.gaussian_kde` with the default bandwidth method (Scott's rule).
   - Evaluate both KDEs on a discrete linear grid from `0` to `2000` (inclusive) with exactly `2000` points. (Hint: use `numpy.linspace(0, 2000, 2000)`).
   - Normalize the evaluated KDE arrays so that they sum to exactly 1.0, creating valid discrete probability mass functions (PMFs) for both distributions over the grid.
   - Calculate the Jensen-Shannon distance between these two PMFs using `scipy.spatial.distance.jensenshannon`.

4. **Save the Output**:
   Write the resulting Jensen-Shannon distance, rounded to exactly 4 decimal places, to a file named `/home/user/jsd_output.txt`.

Ensure all code dependencies (like `scipy` and `numpy`) are installed in your environment before running the Python script.