You are a Machine Learning Engineer responsible for preparing training data for a new sensor-fusion model. Our data lake contains millions of 5-dimensional time-series snippets stored as CSV files. Unfortunately, a subset of the sensors occasionally malfunctioned, producing "corrupted" data windows.

We have a proprietary legacy tool, located at `/app/detector_oracle`, which accurately identifies these corrupted files. It accepts a single CSV file path as an argument. It exits with code `0` if the file is clean, and exits with code `1` if the file is corrupted. Since the tool is a stripped binary, we cannot inspect its source code, and its execution is far too slow for our large-scale data storage pipelines.

Your task is to reverse-engineer the statistical logic of this oracle by treating it as a black box (or reverse-engineering it directly) and implement a high-performance replacement in Rust.

Requirements:
1. Probe the `/app/detector_oracle` to understand its classification boundary. The oracle uses linear algebra, specifically covariance/correlation characteristics between certain features, to detect the anomalies. You may want to generate synthetic data with varying covariance structures and bootstrap samples to determine the exact threshold it uses.
2. Create a Rust project at `/home/user/rust_detector`.
3. Implement the reverse-engineered detection logic in Rust. Your program must accept a single CSV file path as a command-line argument.
4. Your Rust binary must exit with code `0` for clean files and code `1` for corrupted files, exactly mimicking the oracle.
5. Compile your Rust project in release mode so the final executable is at `/home/user/rust_detector/target/release/detector`.

You can use any standard Rust crates (e.g., `csv`, `nalgebra`, `statrs`) by defining them in your `Cargo.toml`. You have access to a few sample CSVs in `/home/user/samples/` to get started, but you will likely need to generate more to fully understand the oracle's decision boundary.