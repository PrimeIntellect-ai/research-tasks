You are an AI assistant acting as a bioinformatics analyst. We are studying the spectral properties of genomic sequences mapped to numerical signals (e.g., Electron-Ion Interaction Pseudopotentials). We have pre-processed a set of 10 DNA numerical signals, each of length 1024, into an HDF5 file. 

Your task is to write a C++ pipeline that performs genomic signal processing and dimensionality reduction on these sequences to identify dominant periodicities (such as the period-3 property of coding regions).

Here is the step-by-step pipeline you must implement:

1. **Install Dependencies**: Install any necessary development libraries for C++. You will need libraries for HDF5 I/O, FFT (e.g., FFTW3), and Linear Algebra (e.g., Eigen3). You have `sudo` privileges for `apt-get`.
2. **Read Data**: Write a C++ program that reads the 2D dataset `/dna_signals` (shape: 10 x 1024, double precision) from `/home/user/sequences.h5`.
3. **Spectral Analysis**: For each of the 10 signals (rows), compute the discrete Fourier transform (1D FFT). Calculate the magnitude spectrum for each signal (i.e., $\sqrt{\text{Re}^2 + \text{Im}^2}$). You will get a 10 x 1024 matrix of magnitude spectra.
4. **Matrix Decomposition**: Perform Singular Value Decomposition (SVD) on this 10 x 1024 magnitude matrix. 
5. **Save Results**: Write the following to a new HDF5 file at `/home/user/results.h5`:
   - A dataset named `/singular_values` containing the 10 singular values (1D array of doubles).
   - A dataset named `/principal_spectrum` containing the *first* right singular vector (the one corresponding to the largest singular value), which represents the dominant spectral pattern across all sequences (1D array of doubles, length 1024).

**Requirements:**
- Use **C++**. Write your code in `/home/user/src/` (you may need to create this directory).
- Provide a `CMakeLists.txt` or `Makefile` to compile your code into an executable named `analyze_spectra`.
- Run your executable so that `/home/user/results.h5` is successfully generated.
- Ensure the output HDF5 file uses standard double-precision float datasets.