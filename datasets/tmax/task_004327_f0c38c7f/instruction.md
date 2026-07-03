You are acting as an MLOps engineer tracking experiment artifacts. We have a Rust-based feature engineering pipeline that calculates the Z-scores (standardized values) of sensor readings. Unfortunately, a recent change introduced a mathematical bug: the pipeline silently produces `NaN` or `0.0` for variances due to catastrophic cancellation and precision loss in floating-point operations.

Your task is to fix this pipeline, run it, and generate the final deterministic artifacts.

1. **Locate the project:** The Cargo project is located at `/home/user/pipeline`.
2. **The Data:** The input dataset is at `/home/user/data/input.csv`.
3. **The Bug:** The current implementation in `/home/user/pipeline/src/main.rs` uses a naive single-pass formula (`E[X^2] - E[X]^2`) with `f32` precision, which fails on our large-magnitude sensor data.
4. **The Fix:** Modify the Rust code to use a numerically stable algorithm (e.g., Welford's online algorithm or a two-pass approach) and use `f64` for all internal mathematical accumulations to avoid precision loss. 
5. **Output Requirements:**
   - Compute the population standard deviation (divide by `N`, not `N-1`).
   - Calculate the Z-score for each row: `(value - mean) / pop_std_dev`.
   - Write the results to `/home/user/pipeline/output.csv`.
   - The output CSV must have exactly three columns: `id`, `sensor_value`, and `z_score`.
   - The `z_score` must be formatted to exactly 4 decimal places (e.g., `1.4142`, `-0.7071`, `0.0000`).
   - The CSV must include a header row.
6. **Artifact Tracking:** To ensure pipeline reproducibility, compute the SHA-256 checksum of `/home/user/pipeline/output.csv` and save the hex-encoded hash to `/home/user/pipeline/artifact_hash.txt`.

Ensure the project builds successfully with `cargo build` and runs correctly. Leave the final `output.csv` and `artifact_hash.txt` in the `/home/user/pipeline` directory.