You are a performance engineer tasked with profiling an acoustic sensor application. The application processes environmental audio and dumps the resulting high-dimensional spectral feature matrices into HDF5 files. Recently, a severe memory leak was introduced that corrupts the low-rank structure of the output matrices, subtly altering their frequency distributions. We need a robust, automated way to filter out these corrupted ("evil") files from the valid ("clean") ones.

You have been provided with:
1. A reference audio profile: `/app/reference_profile.wav` (contains the baseline acoustic signature).
2. A corpus of HDF5 files to classify, located in two directories (for your testing): `/app/corpus/clean/` and `/app/corpus/evil/`.

**Your Objective:**
Write a Python command-line tool at `/home/user/profiler.py` that accepts an HDF5 file path and the reference WAV file path as arguments, and prints either `CLEAN` or `EVIL` to standard output.

**Algorithm Requirements:**
1. **Audio Spectral Analysis:** Read `/app/reference_profile.wav`. Compute its 1D discrete Fourier transform (real FFT) to obtain the magnitude spectrum. Normalize this magnitude spectrum so it sums to 1 (treating it as a probability distribution $P$).
2. **Matrix Extraction:** Read the input HDF5 file. Each file contains a single dataset named `features` (a 2D matrix of shape $N \times M$).
3. **Matrix Decomposition:** Perform Singular Value Decomposition (SVD) on the `features` matrix to obtain the singular values. 
4. **Reshaping & Spectral Comparison:** The corrupted memory leaks cause the singular values to decay much slower. Normalize the singular values to sum to 1 (distribution $Q$). Calculate the Wasserstein distance (Earth Mover's Distance) between the singular value distribution $Q$ and the highest $min(N, M)$ amplitude peaks of the audio's frequency distribution $P$.
5. **Classification:** If the Wasserstein distance exceeds $0.05$, classify the file as `EVIL`. Otherwise, classify it as `CLEAN`.

**Execution Signature:**
Your script must be executable exactly like this:
`python3 /home/user/profiler.py <path_to_h5_file> /app/reference_profile.wav`

The only output to stdout should be the exact string `CLEAN` or `EVIL`. Ensure your code handles the matrix decomposition efficiently. Do not use external libraries beyond `numpy`, `scipy`, `h5py`, and `soundfile`.