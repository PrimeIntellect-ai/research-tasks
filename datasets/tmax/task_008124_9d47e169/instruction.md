You are an MLOps engineer tasked with writing a fast Rust utility to validate experiment artifacts. We have an artifact file containing embedding vectors from a recent model training run, but the training was unstable, resulting in missing values and exploding gradients (outliers).

Your task is to write a Rust program that processes this data, computes a summary metric using linear algebra, and writes the result to a file. 

The input data is located at `/home/user/embeddings.csv`. It contains no header. Each line has exactly 3 comma-separated values representing a 3D vector.

Write and execute a Rust program (you can create a standard Cargo project at `/home/user/artifact_tester`) that performs the following steps:
1. Read `/home/user/embeddings.csv`.
2. Parse each row into a 3D vector of 64-bit floats (`f64`).
3. **Missing Value Handling:** If a value is empty or exactly the string `"NaN"`, replace it with `0.0`.
4. **Outlier Removal:** Calculate the L2 norm (Euclidean norm) of each row vector. If the L2 norm is strictly greater than `10.0`, drop the entire row (do not include it in further calculations).
5. **Feature Extraction:** Compute the center of mass (the mean vector) of all the *remaining* valid rows.
6. **Numerical Accuracy Test:** Calculate the L1 norm (sum of absolute values) of the resulting mean vector.
7. Write the final L1 norm to `/home/user/metric.txt`, formatted to exactly 4 decimal places (e.g., `1.2340`).

Do not use any external crates other than standard Rust library (no `csv`, `ndarray`, etc., just `std::fs`, `std::str`, etc.) to keep the utility dependency-free and fast. Once you have written the code, compile and run it so that `/home/user/metric.txt` is created with the correct value.