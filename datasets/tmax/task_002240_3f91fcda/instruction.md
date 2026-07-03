You are a build engineer responsible for managing artifacts and ensuring the stability of our hybrid Rust-Python data processing pipeline. Our infrastructure relies on a custom Rust dependency analyzer that outputs dependency graphs and memory profiling logs. However, the system is currently broken.

Your task consists of three main parts:

**Part 1: Fix the Vendored Rust Analyzer**
We have vendored a third-party Rust tool called `dep-analyzer-core` (version 1.2.0) located at `/app/dep-analyzer-core`. The original developers introduced a critical bug causing a compilation failure due to a borrow checker/lifetime issue in the graph traversal logic (`src/graph.rs`). 
1. Navigate to `/app/dep-analyzer-core`.
2. Debug and fix the Rust ownership/lifetime issue so that `cargo build --release` completes successfully.
3. Once compiled, run the binary using `./target/release/dep-analyzer-core --generate-samples > /home/user/rust_output.log` to ensure it works.

**Part 2: Build an Artifact Classifier (Python)**
Our CI system produces artifact logs representing the dependency resolution paths and memory usage traces. Some of these logs contain "evil" patterns: cyclic dependencies that crash the resolver, or anomalous memory profiles indicating leaks. 
You must write a Python script at `/home/user/classifier.py` that parses these logs and classifies them as either valid or invalid.
1. The script must take two arguments: the input log file path and the output classification file path.
   Usage: `python3 /home/user/classifier.py <input_log> <output_txt>`
2. The input log is a JSON file containing an array of dependency traversal events and memory snapshots.
3. The script must output a single word to the output file: `CLEAN` if the log is valid, or `EVIL` if the log contains a cycle or a memory leak pattern (defined as memory consumption strictly increasing over 5 consecutive snapshots without a drop).

**Part 3: Batch Processing**
We have provided a corpus of logs in `/home/user/corpora/`.
1. Process all logs in `/home/user/corpora/clean/` and `/home/user/corpora/evil/` using your Python classifier.
2. Write a summary script `run_eval.sh` that iterates over all files in both directories, runs your Python script, and appends the results in CSV format (`filename,classification`) to `/home/user/classification_results.csv`.

Your final solution must flawlessly categorize the logs.