You are a performance engineer tasked with debugging a statistical analysis pipeline. 

We have a vendored third-party Rust library called `fast_solver` located at `/app/fast_solver`. This library calculates specialized convergence metrics on arrays of floating-point numbers. However, the package is currently broken and cannot be compiled. 

First, diagnose and fix the compilation issue in the `fast_solver` package. 

Second, we've noticed that even when the package compiles, it suffers from convergence failures (producing `NaN` or panicking) on certain inputs due to statistical anomalies (e.g., cases where the variance is exactly zero or inputs that trigger divide-by-zero errors in its intermediate assertions). 

Your objective is to build a Rust-based detector that acts as a gatekeeper. Create a new Cargo project at `/home/user/validator`. Write a CLI program that takes a single command-line argument: the absolute path to a text file containing one floating-point number per line. 

Your program must:
1. Read the numbers from the file.
2. Determine if the data will cause a convergence failure in the `fast_solver` logic. You may use `fast_solver` as a dependency or implement the mathematical pre-check yourself.
3. Print exactly `ACCEPT` to standard output if the data is safe to process.
4. Print exactly `REJECT` to standard output if the data exhibits the statistical anomaly that would cause a failure.

Ensure your binary can be compiled with `cargo build --release`. The compiled binary should be located at `/home/user/validator/target/release/validator`.

We have provided sample datasets for you to test against, though the automated verifier will use hidden test cases. 
- Clean, safe data can be found in `/app/corpora/clean/`
- Data known to cause failures can be found in `/app/corpora/evil/`

Your classifier must be perfectly accurate against the verification corpora.