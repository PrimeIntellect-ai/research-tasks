You are a data engineer reviewing a Rust-based data processing pipeline written by a junior analyst. 

The project is located at `/home/user/pipeline`. It reads a dataset from `/home/user/data/input.csv`, performs Z-score normalization (standard scaling) on the `value` column, splits the data into a training set and a testing set, and writes the results to `/home/user/data/train_normalized.csv` and `/home/user/data/test_normalized.csv`.

**The Problem:**
The junior analyst accidentally introduced a data leakage bug. In the current implementation (`/home/user/pipeline/src/main.rs`), the pipeline calculates the mean and standard deviation of the `value` column across the *entire* dataset before splitting it. This leaks information from the test set into the training set's normalization parameters.

**Your Task:**
1. Fix the Rust code in `/home/user/pipeline/src/main.rs` to eliminate the data leakage. 
2. The mean and standard deviation (population standard deviation, divide by N) must be calculated **only** using the training set.
3. Apply these training-derived parameters to normalize the `value` column for *both* the training set and the test set.
4. The train/test split must remain chronological: the first 80% of the rows (excluding the header) are the training set, and the remaining 20% are the test set. (The input has exactly 100 data rows, so 80 for train, 20 for test).
5. Compile the fixed project using `cargo build --release`.
6. Run the compiled binary to generate the corrected output files.

**Output Requirements:**
- `/home/user/data/train_normalized.csv` and `/home/user/data/test_normalized.csv` must be created.
- They must retain the CSV header: `id,category,normalized_value`
- The `normalized_value` should be formatted to 4 decimal places (e.g., `format!("{:.4}", val)` in Rust).
- Do not change any file paths or CSV layouts.

Fix the code, build it, and run the pipeline to produce the un-leaked datasets.