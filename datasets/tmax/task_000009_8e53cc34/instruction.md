You are tasked with replacing a legacy scientific computing module that calculates a custom spectral distance metric between two signals. The original source code was lost, but we have a reference binary and a screenshot of the mathematical definition from an old paper.

Your goal is to write a C program that computes this metric, producing bit-exact identical results to the legacy oracle.

1. **Analyze the Equation**: Inspect the image located at `/app/equation_def.png`. It contains the mathematical definition of the distance metric $D$ based on the Discrete Fourier Transforms (DFT) of two input sequences, $x$ and $y$. 
2. **Implement the Program**: Write a C program that:
   - Takes a single command-line argument: the path to an input binary file.
   - Reads the input file, which contains exactly 512 double-precision floating-point numbers (little-endian, IEEE 754). The first 256 doubles are the signal $x[n]$, and the following 256 doubles are the signal $y[n]$. Thus, $N=256$.
   - Computes the distance metric $D$ as defined in the image. 
   - Prints the final scalar value $D$ to standard output using the format specifier `"%.15e\n"`.
3. **Compilation**: Save your source code in `/home/user/` and compile it to an executable named `/home/user/compute_metric`. You may use standard libraries (`math.h`, etc.).
4. **Reproducibility Constraints**: 
   - To match the legacy oracle (`/app/oracle_bin`), you must use the naive $O(N^2)$ DFT implementation. Do not use FFTW or other optimized libraries, as floating-point associativity will cause slight differences.
   - Accumulate the DFT sums and the final outer distance sum strictly sequentially in ascending index order (from 0 to $N-1$) using `double` precision. Do not use OpenMP reductions or parallel accumulators for the summations, as this will alter the floating-point reduction order and fail the bit-exactness verification.

The automated verification system will randomly generate multiple binary input files and run both your `/home/user/compute_metric` and the `/app/oracle_bin` to ensure the outputs are strictly identical.