You are a data scientist stepping into a project where a previous engineer left a broken data cleaning and dimensionality reduction pipeline. 

The pipeline is written in Rust and is located at `/home/user/pca_cleaner`. It reads a 4-dimensional dataset from `/home/user/data/measurements.csv` and projects it onto a 2D plane using a predefined projection matrix.

Currently, the pipeline has two critical flaws:
1. **Schema Enforcement Failure**: The dataset contains some corrupted rows with strings like "ERR" or "N/A" instead of valid floating-point numbers. The current script parses these as `NaN`, causing the output to be filled with `NaN`s. You need to enforce the data schema by completely skipping any row that contains non-parseable floating-point values in any of its 4 feature columns.
2. **Numerical Accuracy Bug**: Dimensionality reduction (like PCA) requires the data to be mean-centered before projection, but the current code projects the raw data directly. You must modify the code to calculate the mean for each of the 4 features across all *valid* rows, and then mean-center the valid rows (subtract the respective feature mean from each feature) *before* applying the projection matrix.

Your task:
- Fix the Rust code in `/home/user/pca_cleaner/src/main.rs`.
- Run the compiled Rust program to generate the output file at `/home/user/projected.csv`.
- The output file must be a CSV with the header `id,p1,p2`.
- `p1` and `p2` must be formatted to exactly 4 decimal places.
- The `id` should be preserved from the original valid rows.

You can run `cargo build` and `cargo run` inside `/home/user/pca_cleaner` to test your changes.