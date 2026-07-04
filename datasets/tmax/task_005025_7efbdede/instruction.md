I am working on fitting a spectral decomposition model to some experimental acoustics data. We rely on a proprietary C library, `libspecfact-1.2.0`, to perform a specialized non-negative matrix factorization. Unfortunately, we recently migrated our workspace and the library fails to build. Furthermore, the factorization often crashes with a divide-by-zero or non-convergence error when the input spectra contain near-singular (zero or flat) regions.

Here is what you need to do:

1. **Fix and Build the Library:**
   The source code for the library is located in `/app/libspecfact-1.2.0`. It contains a `Makefile`. We need it built as a shared library (`libspecfact.so`). There is a perturbation in the `Makefile` preventing this (likely related to position-independent code and missing math link flags). Fix the `Makefile` and compile `libspecfact.so`.

2. **Develop the Multi-Language Pipeline:**
   Create an executable Python script at `/home/user/pipeline.py`. It should take exactly two command-line arguments: an input file path and an output file path.
   `./pipeline.py <input.bin> <output_W.bin>`

   The pipeline must perform the following steps:
   - **Load & Reshape:** Read the `<input.bin>` file, which contains exactly 65,536 `float64` values (little-endian, 524,288 bytes). Reshape this 1D array into a 256x256 2D matrix (representing time vs. spatial data).
   - **Fourier Transform:** Apply a 2D Discrete Fourier Transform (using `numpy.fft.fft2`) to the 256x256 matrix. Compute the magnitude spectrum (absolute value of the complex output).
   - **Regularization (Anchor Fix):** To prevent the matrix factorization from failing on near-singular inputs, add a regularization constant of exactly `1e-6` to every element in the magnitude spectrum.
   - **C-Library Integration:** Load the compiled `/app/libspecfact-1.2.0/libspecfact.so` using `ctypes`. The library exposes a function:
     `void factorize(double* matrix, int rows, int cols, int k, double* w_out, double* h_out)`
     Pass your 256x256 regularized magnitude spectrum to this function to extract `k=4` components. You will need to allocate memory for `w_out` (256x4) and `h_out` (4x256) and pass their pointers.
   - **Quantization & Output:** Take the resulting `W` matrix (256x4), scale it by multiplying by 255.0, clip the values to the range [0, 255], and cast it to unsigned 8-bit integers (`uint8`). Save this raw binary `uint8` array (exactly 1024 bytes) to the `<output_W.bin>` path.
   - **Visualization:** Generate a line plot of the 4 columns of the `W` matrix and save it as `/home/user/visualization.png`. Ensure it has a legend and axis labels.

Make sure your script is robust and deterministic. Our automated testing pipeline will run your script against many random input files and rigorously compare the binary outputs to our reference implementation.