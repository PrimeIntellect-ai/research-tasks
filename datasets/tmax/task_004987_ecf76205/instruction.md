You are a data engineer tasked with fixing a broken Rust-based ETL and modeling pipeline. 

You have been given a Rust project located at `/home/user/rust-etl`. This pipeline reads a dataset (`data.csv`), applies Principal Component Analysis (PCA) for dimensionality reduction, trains a Linear Regression model, calculates the Mean Squared Error (MSE) on the training set, and plots the predictions vs. true values to a file named `plot.png`.

Currently, the pipeline has three major issues:
1. **Blank Plot:** The script attempts to use the `plotters` crate to generate `plot.png`, but due to a missing backend finalization step (similar to a misconfigured backend), the generated image file is corrupted or incomplete. 
2. **Poor Numerical Accuracy:** The PCA is currently hardcoded to reduce the data to 1 component. This throws away too much information, causing the model's MSE to be unacceptably high. The test suite in `src/main.rs` requires the MSE to be strictly less than 2.0.
3. **Missing Metrics Output:** The pipeline does not write out the final metrics as required by our downstream systems.

Your task is to:
1. Fix the plotting logic in `src/main.rs` so that `plot.png` is correctly written and finalized (ensure the drawing area is properly presented/dropped).
2. Adjust the PCA `n_components` parameter in `src/main.rs` so that the numerical accuracy test (`cargo test`) passes. You should find the minimal number of components that brings the MSE under 2.0.
3. Modify the end of the `main` function to output a JSON file at `/home/user/rust-etl/metrics.json` containing the calculated MSE. The format must be exactly: `{"mse": 1.234}` (with the actual float value).
4. Run `cargo build`, `cargo test`, and `cargo run` successfully.

Ensure `/home/user/rust-etl/metrics.json` and `/home/user/rust-etl/plot.png` are present and valid when you finish.