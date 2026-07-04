You are a performance engineer tasked with creating a highly optimized, parallelized simulation and signal processing pipeline. 

Your objective is to write a C program that simulates the 1D wave equation (a PDE) for multiple initial conditions, extracts a time-series signal at a specific spatial point, processes the signal using a Fast Fourier Transform (FFT) to get its frequency spectrum, normalizes it into a probability distribution, and calculates the Kullback-Leibler (KL) divergence against a uniform distribution.

Since you do not have root access, you must first download, compile, and install the FFTW library locally in your home directory before writing and compiling your C program.

**Phase 1: Dependency Installation**
1. Download FFTW 3.3.10 from `https://www.fftw.org/fftw-3.3.10.tar.gz`.
2. Extract and compile it from source.
3. Install it locally to the prefix `/home/user/fftw`.

**Phase 2: The C Program (`/home/user/wave_profiler.c`)**
Write a C program that performs `N_sim = 50` independent simulations. You must parallelize the loop over the 50 simulations using OpenMP to ensure the profiling runs efficiently.

Simulation parameters:
- Space grid size: `Nx = 1000`
- Time steps: `Nt = 2000`
- Constant: `C2 = 0.25` (This represents `(c * dt / dx)^2`)

For each simulation `s` (from `0` to `49`):
1. **Initialization:**
   - Create a 2D array `u[Nt][Nx]` initialized to 0.0.
   - For `x` from `0` to `Nx-1`, set the initial conditions for `t=0` and `t=1`:
     `source_pos = s * 20`
     `u[0][x] = exp( - pow(x - source_pos, 2) / 50.0 )`
     `u[1][x] = u[0][x]`
   - Boundary conditions are always `0.0` at `x=0` and `x=Nx-1`.

2. **PDE Numerical Solving:**
   - For `t` from `1` to `Nt - 2`, and `x` from `1` to `Nx - 2`, advance the wave equation:
     `u[t+1][x] = 2.0 * u[t][x] - u[t-1][x] + C2 * (u[t][x+1] - 2.0 * u[t][x] + u[t][x-1])`

3. **Signal Extraction & Spectroscopy:**
   - Extract the signal `A[t] = u[t][500]` for `t` from `0` to `Nt-1`.
   - Use FFTW to compute the 1D discrete Fourier transform of the real array `A` (size `Nt`). You can use a complex-to-complex transform or real-to-complex transform, but ensure you compute the magnitude correctly for `Nt` bins. If you use standard complex transform, treat `A` as the real part and set imaginary part to `0.0`.
   - Calculate the power spectrum `M[k] = Re(X[k])^2 + Im(X[k])^2` for `k` from `0` to `Nt-1`.
   - To avoid division by zero later, add `1e-9` to every `M[k]`.

4. **Probability Distribution Distance:**
   - Normalize `M` so it sums to `1.0`, creating a probability distribution `P[k]`.
   - Define a reference uniform distribution `Q[k] = 1.0 / Nt`.
   - Calculate the KL divergence for this simulation: `KL_s = sum_{k=0}^{Nt-1} ( P[k] * log(P[k] / Q[k]) )`. (Use the natural logarithm).

**Phase 3: Aggregation and Output**
- Calculate the average KL divergence across all 50 simulations.
- Write ONLY this average KL divergence formatted to 6 decimal places (e.g., `1.234567`) to the file `/home/user/result.txt`.

**Phase 4: Compilation and Execution**
Compile your program using `gcc`, linking against your locally installed FFTW library (`-I/home/user/fftw/include` and `-L/home/user/fftw/lib`) and using OpenMP (`-fopenmp`). Ensure you also link the math library (`-lm`). 
Run your program to produce the `/home/user/result.txt` file.