You are a Machine Learning Engineer preparing a training dataset for a new model. The raw sensor data is provided as a CSV file, but the feature extraction pipeline requires applying numerical differentiation, covariance computation, and matrix factorization. Some of the input signal matrices are near-singular, which previously caused the factorization step to crash in production.

Your task is to build a reproducible data processing pipeline in **Rust** that robustly extracts features from the dataset without crashing.

**Input Data:**
A dataset located at `/home/user/dataset.csv` contains 100 rows. Each row consists of 25 comma-separated floating-point numbers, representing a flattened 5x5 matrix $M$ (row-major order).

**Pipeline Specifications:**
Create a Rust project in `/home/user/feature_extractor`. Your Rust program must process each row in the CSV sequentially and perform the following mathematical operations:

1. **Reshape:** Parse the 25 floats into a 5x5 matrix $M$.
2. **Numerical Differentiation:** Compute the gradient matrix $G$ using a simple backward difference along the rows (axis 0):
   - For $i > 0$: $G_{i,j} = M_{i,j} - M_{i-1,j}$
   - For $i = 0$: $G_{0,j} = 0$
3. **Covariance Matrix:** Compute the matrix $C = G^T G$ (where $G^T$ is the transpose of $G$).
4. **Regularization:** Because some input matrices represent stationary signals, $C$ can be near-singular or singular. To prevent factorization failures, apply Tikhonov regularization by adding a ridge:
   $C_{reg} = C + \alpha I$
   where $I$ is the 5x5 identity matrix and $\alpha = 0.01$.
5. **Factorization:** Compute the Cholesky decomposition of $C_{reg}$ such that $C_{reg} = L L^T$, where $L$ is the lower triangular matrix.
6. **Feature Extraction:** Calculate the trace (sum of the main diagonal elements) of the lower triangular matrix $L$.

**Output:**
Your Rust program should write the resulting 100 trace values to `/home/user/features.txt`.
- Write one float per line, corresponding to the rows in the input CSV.
- Each float must be formatted to exactly 4 decimal places (e.g., `12.3456`).

**Constraints:**
- You must use **Rust** to perform the computations. You may use any standard Rust crates for linear algebra (e.g., `nalgebra`, `ndarray`, `ndarray-linalg`) by setting up a standard `Cargo.toml`.
- Ensure your code handles the file I/O properly and implements the exact mathematical sequence described to maintain reproducibility.