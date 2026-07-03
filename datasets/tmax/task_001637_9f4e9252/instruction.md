You are a machine learning engineer preparing feature data for a protein classification model. Your goal is to extract spectral features from a set of protein sequences using their hydrophobicity profiles.

You need to write a Python script that parses a FASTA file, performs spectral analysis, and calculates numerical integrals to form the final feature set. 

Here are the exact requirements:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv`. Activate it and install `numpy` and `scipy`. All your Python execution should use this environment.

2. **Input Data**:
   There is a FASTA file located at `/home/user/proteins.fasta` containing several protein sequences.

3. **Sequence Encoding**:
   Parse the FASTA file. For each sequence, map the amino acid characters to their Kyte-Doolittle hydrophobicity values to create a 1D numerical array. 
   Use the following mapping:
   A: 1.8, R: -4.5, N: -3.5, D: -3.5, C: 2.5, Q: -3.5, E: -3.5, G: -0.4, H: -3.2, I: 4.5, L: 3.8, K: -3.9, M: 1.9, F: 2.8, P: -1.6, S: -0.8, T: -0.7, W: -0.9, Y: -1.3, V: 4.2

4. **Spectral Analysis**:
   For each numerical sequence (length $N$):
   - Compute the 1D Discrete Fourier Transform (FFT) using `numpy.fft.fft`.
   - Calculate the Power Spectrum $P$ by taking the squared magnitude of the FFT output: $P[k] = |X[k]|^2$.
   - Extract the positive frequency components, *excluding* the DC component (index 0). Specifically, slice the array from index 1 to $\lfloor N/2 \rfloor$ (inclusive). Let's call this array $P_{pos}$.

5. **Numerical Integration**:
   - Compute the "Total Spectral Energy" for each protein by numerically integrating the $P_{pos}$ array. 
   - Use the composite trapezoidal rule (`numpy.trapz` or `scipy.integrate.trapezoid`) across the array elements (assume default spacing `dx=1.0`).

6. **Output**:
   Generate a CSV file at `/home/user/features.csv` with exactly two columns: `Sequence_ID` (the FASTA header without the `>` character) and `Total_Energy` (rounded to 2 decimal places).

Please create the script, run it, and ensure `/home/user/features.csv` is correctly populated.