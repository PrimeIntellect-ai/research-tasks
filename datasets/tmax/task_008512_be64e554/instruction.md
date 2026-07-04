You are an ML engineer preparing training data. The data preprocessing pipeline has a Rust application that generates feature aggregates. However, you've noticed that running the tool multiple times produces slightly different outputs, breaking your regression tests and causing non-reproducible model training. This is due to a floating-point reduction order issue caused by a naive parallel summation using a `Mutex`.

Your tasks are:
1. Navigate to the Rust project located at `/home/user/data_gen`.
2. Modify the source code in `src/main.rs` to fix the non-determinism. Specifically, change the parallel `for_each` and `Mutex` implementation to use a purely **sequential** iterator and reduction (`iter().map(...).sum::<f64>()`) to ensure the floating-point addition order is strictly left-to-right. 
3. Recompile the scientific tool from source using `cargo build --release`.
4. Run the compiled binary. It will read `/home/user/input_data.csv` and write its output to `/home/user/output_features.csv`.
5. Compare your output against the reference dataset located at `/home/user/reference_features.csv`. They must match exactly (string-wise).
6. Create a log file at `/home/user/regression_result.txt` containing only the word `PASS` if the outputs match, followed by a newline, and then the exact output floating-point value on the second line.

Ensure you do not change the mathematical operations being applied (e.g., `.sin()`), only the iteration and reduction strategy.