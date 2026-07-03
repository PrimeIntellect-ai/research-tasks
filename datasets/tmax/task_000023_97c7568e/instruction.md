You are a machine learning engineer preparing structural biology data for a 3D graph neural network. Your data pipeline extracts atomic coordinates from PDB files, calculates their 3x3 spatial covariance matrix, and performs a Cholesky decomposition to generate rotationally invariant spatial features. 

However, your Rust-based pipeline is crashing. It fails on molecules that are perfectly planar (e.g., strictly 2D structures), which produce a near-singular covariance matrix that causes the Cholesky decomposition to panic.

You will find the Rust project at `/home/user/pdb_feature_extractor` and a failing input file at `/home/user/input.pdb`.

Your tasks:
1. **Fix the Pipeline**: Modify `/home/user/pdb_feature_extractor/src/main.rs`. Catch the case where `nalgebra`'s `cholesky()` fails (returns `None`). When this happens, add a "jitter" of exactly `1e-5` to each diagonal element of the covariance matrix, and recompute the Cholesky decomposition.
2. **Regression Testing**: Add a Rust unit test inside `src/main.rs` named `test_planar_jitter`. This test should programmatically create a 3x3 covariance matrix representing a flat plane (e.g., `[[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0]]`), apply your jitter logic, and assert that the resulting Cholesky lower-triangular matrix $L$ can be successfully extracted.
3. **Execute & Output**: Run your fixed program on `/home/user/input.pdb`. The program should calculate the trace (the sum of the main diagonal elements) of the resulting lower-triangular matrix $L$. Save this single float value to `/home/user/feature_trace.txt`.

Ensure `cargo test` passes and `cargo run` cleanly processes the file and generates the correct output.