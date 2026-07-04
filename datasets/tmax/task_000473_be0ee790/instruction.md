You are an AI assistant helping a computational researcher run matrix simulations. 

We are using a vendored Go math package located at `/app/numgo`. This package provides a Cholesky decomposition routine. However, it currently fails or returns NaNs on near-singular input matrices. The package's `README.md` notes that for stability, the `Cholesky` algorithm should regularize the diagonal by enforcing a minimum value of `1e-10` before taking the square root during the factorization (i.e., if the term inside the square root is less than `1e-10`, it should be clamped to `1e-10`). This perturbation was accidentally removed or misconfigured in `/app/numgo/cholesky.go`.

Your tasks:
1. Inspect and fix the vendored package `/app/numgo/cholesky.go` so it properly regularizes near-singular matrices according to the `README.md`.
2. Write a Go program at `/home/user/runner.go` that:
   - Reads an integer `N` from standard input, representing the dimension of an `N x N` matrix.
   - Reads the next `N` lines from standard input, each containing `N` space-separated floating-point numbers representing the matrix elements.
   - Computes a scaling factor `C`, defined as the numerical average of the absolute values of all *off-diagonal* elements.
   - Adds `C` to each *diagonal* element of the matrix (this is a simplistic distribution fitting to ensure positive-definiteness).
   - Computes the Cholesky decomposition `L` of this modified matrix using the fixed `numgo` package.
   - Prints the resulting lower-triangular matrix `L` to standard output. Print each row on a new line, with elements space-separated and formatted to exactly 6 decimal places (e.g., `fmt.Printf("%.6f ", val)`).

Build your program so the executable is at `/home/user/runner`.

An automated test suite will verify your work by compiling your code and randomly fuzzing your `/home/user/runner` executable with thousands of near-singular matrices, comparing its output bit-for-bit against a known-good oracle.