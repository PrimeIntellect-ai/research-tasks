You are an acoustic physics researcher tasked with analyzing simulation data to find the dominant spatial modes at the resonant frequency of an acoustic cavity. You have been provided with a proprietary, compiled simulation engine located at `/app/wave_sim`. 

Your objective is to generate the data, process it in the frequency domain, extract the dominant spatial matrix, and decompose it to find its singular values. 

Follow these steps exactly:

1. **Generate Data:** 
   Run the simulator using the command: 
   `/app/wave_sim 64 64 512 /home/user/wave_data.bin`
   This will output a raw binary file containing 32-bit floating-point (float32) values. The data represents a 3D grid `[nx=64][ny=64][nt=512]`, stored contiguously in row-major order (meaning the time dimension `nt` varies fastest, then `ny`, then `nx`).

2. **Develop a C++ Analysis Pipeline:**
   Write a C++ program (e.g., `analyze.cpp`) to process `wave_data.bin`. You are encouraged to use standard scientific libraries such as `Eigen3` for matrix operations, `FFTW3` for Fourier transforms, and the `HDF5` C/C++ API for I/O. You may need to install these via your system's package manager.

3. **Spectral Analysis:**
   - Read the binary data into memory.
   - For each spatial point `(x, y)`, compute the 1D Discrete Fourier Transform (DFT) along the time dimension (`nt`).
   - Calculate the total energy (sum of the squared magnitudes of the complex Fourier coefficients across all `64x64` spatial points) for each frequency index.
   - Identify the peak frequency index `k_peak` that contains the maximum total energy. **Ignore the DC component (index 0)** and only search the positive frequencies (`1 <= k < nt/2`).

4. **Matrix Decomposition:**
   - Extract the `64x64` complex spatial matrix corresponding to the frequency index `k_peak`.
   - Perform a Singular Value Decomposition (SVD) on this complex matrix to compute its singular values.

5. **Export Results:**
   - Extract the 3 largest singular values.
   - Save these 3 values (in descending order) as double-precision floats (64-bit) into an HDF5 file located at `/home/user/results.h5`.
   - The values must be stored in a 1D HDF5 dataset named exactly `/top_svals`.

Compile your C++ program, run it, and ensure `/home/user/results.h5` is created with the correct data.