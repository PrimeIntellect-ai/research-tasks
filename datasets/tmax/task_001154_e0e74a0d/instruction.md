I am an MLOps engineer tracking experimental artifacts. We've discovered a data leakage issue in our previous pipeline where standard scaling was applied to an entire dataset (both train and test) rather than fitting solely on the training data. I need you to perform a two-phase task to analyze our new video data and rewrite our scaling tool in Rust to fix this leak.

**Phase 1: Video Feature Extraction**
We have an experiment recording located at `/app/experiment.mp4`. 
1. Process this video to extract the average grayscale brightness (pixel intensity) for every single frame. 
2. Count the exact number of frames where the average grayscale brightness is strictly greater than 100.0.
3. Write this single integer count to `/home/user/bright_frames.txt`.

**Phase 2: Fixing the Leak with a Rust Tool**
Our tabular datasets come with two columns: `group` (0 for train, 1 for test) and `value` (a floating-point number).
Create a new Rust project at `/home/user/scaler/`. Write a program that:
1. Reads CSV data from standard input (`stdin`). The first line is guaranteed to be the header `group,value`.
2. Computes the mean and population standard deviation (divide by N, not N-1) of `value` using ONLY the rows where `group == 0` (the training set).
3. Applies standard scaling `(value - mean_0) / std_0` to the rows where `group == 1` (the test set).
4. Prints the scaled values for `group == 1` (in the order they appeared) to `stdout` as a JSON array of floats (e.g., `[-1.2, 0.5, 3.1]`). 
5. If there are no `group == 0` rows, or if their standard deviation is exactly 0.0, output `0.0` for all `group == 1` scaled values.
6. The Rust tool should cleanly handle standard formatting and ignore empty lines.
7. Build the tool in release mode so the executable is located exactly at `/home/user/scaler/target/release/scaler`.

Do not use external crates for the math operations; implement the mean and standard deviation logic yourself. You may use `serde_json` and `csv` if you configure them in your `Cargo.toml`.