You are tasked with fixing and heavily optimizing a code complexity analyzer tool for a multi-file project. The analyzer must be written entirely using Bash and standard Linux CLI tools (coreutils, awk, sed, grep, find, etc.). 

Currently, there is a large directory `/home/user/rust_project/` containing 10,000 mock `.rs` files that simulate a Rust project failing to compile due to intricate lifetime issues.
Each file contains a header comment with structured metadata in the following format:
```rust
// Metadata:
// Lifetimes: <number>
// Variables: <number>
// Functions: <number>
```

Your objective is to:
1. Examine the image located at `/app/formula_spec.png` (using tools like `tesseract` if needed). It contains the mathematical formula to compute the "Complexity Score" of a file based on its `Lifetimes`, `Variables`, and `Functions` counts.
2. Write a highly optimized Bash script at `/home/user/analyze.sh` that processes all `.rs` files in `/home/user/rust_project/`.
3. For each file, parse the metadata, evaluate the mathematical expression described in the image, and output the result.
4. Your script must output a CSV file at `/home/user/complexity_scores.csv` with the format `filename,score` (where filename is just the basename of the file, e.g., `file_123.rs`), sorted alphabetically by filename.
5. **Performance matters.** A naive Bash `while read` loop will be far too slow. You must design an efficient structured data parsing and evaluation pipeline (e.g., using `awk` or `xargs`). Your script's execution time will be measured, and it must process all 10,000 files very quickly to pass the automated metric threshold.

Make sure `/home/user/analyze.sh` is executable and does not require any interactive input. When executed, it should independently read the files and generate `/home/user/complexity_scores.csv`.