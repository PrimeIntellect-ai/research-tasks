I need you to help me analyze a protein backbone structure using spectral analysis. I have an artificial protein structure file located at `/home/user/helix.pdb`.

Please write a C program that performs the following steps:
1. Parse the PDB file and extract the 3D coordinates (X, Y, Z) of all atoms where the atom name is exactly `CA` (Alpha Carbon). Ignore all other atoms. The file contains a single continuous chain.
2. Create a 1D discrete signal $S[n]$ representing the X-coordinate of the $n$-th CA atom (where $n$ starts at 0 for the first CA atom found).
3. Implement a 1D Discrete Fourier Transform (DFT) to compute the frequency spectrum of this signal. **Do not use any external libraries** for the Fourier transform (e.g., no FFTW). You must implement the DFT or FFT yourself using only the standard C math library (`<math.h>`).
4. Calculate the power spectrum $P[k] = \text{Re}(X[k])^2 + \text{Im}(X[k])^2$ for each frequency bin $k$.
5. Find the frequency index $k_{max}$ that has the highest power, considering only $0 < k < N/2$ (ignore the DC component at $k=0$ and the symmetric upper half).
6. Print $k_{max}$ to standard output and also write this single integer to a file named `/home/user/peak_frequency.txt`.

Save your C code to `/home/user/spectral_analysis.c`.
Compile it using: `gcc -O3 -o /home/user/analyzer /home/user/spectral_analysis.c -lm`
Then execute it so that the output file is generated.