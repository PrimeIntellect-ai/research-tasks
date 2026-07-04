You are a data engineer responsible for rewriting a fragile ETL pipeline component in Rust. 

The previous Python implementation suffered from "data leakage" between the train and test sets because it normalized batches dynamically (e.g., using `fit_transform` on every chunk). To enforce a strict, stateless transformation, we are shifting to a deterministic random projection for dimensionality reduction.

We need a high-performance Rust CLI tool that reads streaming vector data, applies a fixed projection matrix to reduce its dimensionality, and writes the results to standard output. 

Your tasks are:
1. **Retrieve the Configuration**: 
   There is an image file located at `/app/params.png` containing the configuration for the pipeline. You must extract the `ETL_SEED` value from this image (you may use `tesseract` or any other tool).

2. **Implement the Dimensionality Reduction in Rust**:
   Create a new Cargo project at `/home/user/processor`.
   Write a Rust program that reads lines from standard input. Each line will contain exactly 8 space-separated 64-bit floats.
   
   To avoid relying on external crates for random number generation (which might change their algorithms), you must generate the $8 \times 3$ projection matrix $P$ using a strict Linear Congruential Generator (LCG) initialized with the `ETL_SEED` extracted from the image.
   
   **LCG Formula**:
   - $X_0 = \text{ETL\_SEED}$
   - $X_{n+1} = (1103515245 \times X_n + 12345) \pmod{2^{31}}$
   
   **Matrix Generation**:
   Generate the $8 \times 3$ matrix $P$ in row-major order (row 0 col 0, row 0 col 1, row 0 col 2, row 1 col 0, etc.).
   For each element:
   - Compute the next $X$ using the LCG.
   - The matrix value is $V = (X \text{ as f64} / 2147483648.0) \times 2.0 - 1.0$.

   **Transformation**:
   For each 8-dimensional input vector $U$, compute the 3-dimensional output vector $W = U \times P$.
   
3. **Output Format**:
   For each input line, print the resulting 3-dimensional vector $W$ to standard output as space-separated floats, rounded to exactly 4 decimal places (e.g., `1.2345 -0.1234 0.0000`).

4. **Build**:
   Compile your project in release mode so the executable is available at `/home/user/processor/target/release/processor`.

Make sure your code strictly avoids any batch-level statistics. The matrix $P$ must be generated exactly once per run.