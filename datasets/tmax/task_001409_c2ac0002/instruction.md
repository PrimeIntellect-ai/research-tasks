You are a performance engineer tasked with profiling and fixing a molecular network PDE solver pipeline. The solver relies heavily on Cholesky decomposition for solving large systems of normal equations. Recently, the pipeline has been crashing with fatal errors because it encounters near-singular or indefinite input matrices. 

Your objective is to write a pre-filter utility in **Go** that detects and rejects these "ill-conditioned" matrices before they reach the main pipeline solver. 

Here are the requirements for your task:

1. **Parameter Extraction:**
   There is a legacy screenshot of the mathematical formulation saved at `/app/formula.png`. You must use OCR (`tesseract` is preinstalled) to extract the text from this image. The image contains a specific configuration string indicating a `DAMPING` factor. You must extract this exact numerical value.

2. **Filter Implementation (`/home/user/check_matrix.go`):**
   Write a self-contained Go command-line tool that takes a single argument: the path to a CSV file representing a square symmetric matrix.
   - The tool must read and parse the CSV into an $N \times N$ matrix of `float64`.
   - Add the `DAMPING` factor (extracted from the image) to the main diagonal of the matrix. This is a common regularization technique for reproducible computation pipelines.
   - Implement a standard Cholesky decomposition algorithm ($A = L L^T$) in Go. 
   - If the damped matrix is positive definite (the Cholesky decomposition succeeds without encountering zero or negative diagonal elements before taking the square root), the program must terminate with **exit code 0** (Accept).
   - If the matrix is NOT positive definite (Cholesky fails), the program must terminate with an **exit code > 0** (Reject).
   - Do NOT use external third-party matrix libraries for the decomposition; implement the numerical solving algorithm using the Go standard library.

3. **Adversarial Verification Corpus:**
   We have prepared two datasets of matrix CSV files to test your filter:
   - `/app/corpus/clean/`: Contains matrices that are structurally sound and positive definite *after* damping is applied. Your program MUST accept all of these (exit code 0).
   - `/app/corpus/evil/`: Contains matrices that are near-singular or indefinite and remain non-positive definite even after damping. Your program MUST reject all of these (exit code > 0).

Your final deliverable is the Go script at `/home/user/check_matrix.go`. Once you have written and tested it, ensure it successfully processes both corpora according to the exit code rules.