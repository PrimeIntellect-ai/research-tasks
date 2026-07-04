You are a bioinformatics analyst investigating hidden periodicities in a DNA sequence using spectral analysis and Monte Carlo simulations. 

Your objective is to build a toolchain in C that analyzes a DNA sequence, identifies its dominant frequency using a Fourier transform, and computes the statistical significance (p-value) of this periodicity.

Here are your instructions:

1. **Build FFTW3 from source**:
   - An archive of FFTW3 is located at `/home/user/fftw-3.3.10.tar.gz`.
   - Extract it, compile it, and install it with the prefix `/home/user/fftw_install`. Use only the standard `configure`, `make`, and `make install` steps for a static/shared library build.

2. **Write the Analysis Program**:
   - Create a C program at `/home/user/analyze.c`.
   - The program must read a 1024-character DNA sequence from `/home/user/sequence.txt`.
   - Map the sequence into an array of `double` using the following numerical encoding: `A=1.0, C=2.0, G=3.0, T=4.0`.
   - Use the installed FFTW3 library (specifically `fftw_plan_r2c_1d` with `FFTW_ESTIMATE`) to compute the 1D real-to-complex discrete Fourier transform of the sequence.
   - Calculate the magnitude ($ \sqrt{real^2 + imag^2} $) for frequency bins 1 through 512 (ignore the DC component at index 0).
   - Find the maximum magnitude, $M_{orig}$.

3. **Perform Monte Carlo Simulation**:
   - To test the null hypothesis that the periodicity is due to chance, you will shuffle the numerical sequence 1000 times.
   - **Crucial**: To ensure reproducibility, implement the following pseudo-random number generator (PRNG) exactly as shown:
     ```c
     unsigned int my_seed = 42;
     int my_rand() {
         my_seed = (my_seed * 1103515245 + 12345) & 0x7fffffff;
         return my_seed;
     }
     ```
   - For each of the 1000 iterations, apply the Fisher-Yates shuffle to the 1024-element numerical array. Iterate `i` from 1023 down to 1. For each `i`, pick an index `j = my_rand() % (i + 1)`, and swap the elements at indices `i` and `j`.
   - After each shuffle, compute the FFT using FFTW3 as before, and find the maximum magnitude $M_{sim}$ among bins 1 through 512.
   - Count how many times $M_{sim} \ge M_{orig}$. Let this be `K`.
   - Calculate the empirical p-value as $P = K / 1000.0$.

4. **Output and Compilation**:
   - Write the results to `/home/user/results.log` in exactly this format:
     `Max_Mag: <M_orig rounded to 2 decimal places>, P-value: <P rounded to 3 decimal places>`
   - Compile your program into `/home/user/analyze`, linking against your local FFTW3 installation (`-I/home/user/fftw_install/include -L/home/user/fftw_install/lib -lfftw3 -lm`). Run it to produce the log.