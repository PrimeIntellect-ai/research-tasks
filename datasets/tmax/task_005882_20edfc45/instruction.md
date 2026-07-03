You are a bioinformatics analyst tasked with converting a raw DNA sequence into a pseudo-spectroscopic signal to analyze its structural properties. 

Write a C program that performs the following steps:

1. **FASTA Parsing**: Read a DNA sequence from `/home/user/dna.fasta`. Ignore header lines starting with `>` and any newline characters to form a single continuous string of length `N`.
2. **Signal Mapping**: Convert the DNA sequence into a numeric array `X` of type `double`, using the following mapping:
   - A = 1.0
   - C = 2.0
   - G = 3.0
   - T = 4.0
   (Assume the sequence only contains these four characters).
3. **Parallel Signal Filtering**: Apply a convolution filter to array `X` to produce a new array `Y` of length `N`. Use **OpenMP** to parallelize this loop.
   The filter equation is:
   `Y[i] = X[i-1] + 2.0 * X[i] + X[i+1]` for `i = 0` to `N-1`.
   *Boundary conditions:* If `i-1 < 0` or `i+1 >= N`, treat the out-of-bounds `X` values as `0.0`.
4. **Numerical Integration**: Compute the area under the curve of the filtered signal `Y` using the Composite Trapezoidal Rule, assuming a uniform grid spacing of `h = 1.0`. 
   The trapezoidal rule formula is:
   `Integral = (Y[0] / 2.0) + sum_{i=1}^{N-2}(Y[i]) + (Y[N-1] / 2.0)`

Your C program should be saved as `/home/user/process.c`. 
Compile it (make sure to link OpenMP properly) and run it. 
The program must write the final integrated value, formatted to exactly one decimal place (e.g., `123.4`), to the file `/home/user/integral_result.txt`.