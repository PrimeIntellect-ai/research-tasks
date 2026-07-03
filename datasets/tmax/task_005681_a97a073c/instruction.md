You are a performance engineer working on a bioinformatics pipeline. We have a Rust application located at `/home/user/sequence_aligner` that performs sequence alignment, primer design checks, and calculates statistical confidence intervals using a bootstrap method. 

Currently, the bootstrap confidence interval calculation is extremely slow, and we need you to profile, optimize, and test it.

Your task consists of the following steps:
1. **Analyze and Optimize**: Review the Rust source code in `/home/user/sequence_aligner/src/bootstrap.rs`. There is a severe memory allocation bottleneck inside the bootstrap sampling loop that is slowing down the application. Identify the redundant cloning/allocation and modify the Rust code to fix this performance bug without changing the mathematical outcome.
2. **Compile**: Compile the scientific software from source using `cargo build --release` in the `/home/user/sequence_aligner` directory.
3. **Verify Correctness**: The application is hardcoded with a fixed random seed for reproducibility. When you run `/home/user/sequence_aligner/target/release/sequence_aligner`, it will output a 95% Bootstrap Confidence Interval for the alignment scores.
4. **Create a Test Harness**: Write a bash script at `/home/user/run_tests.sh` that:
   - Compiles the application in release mode.
   - Runs the optimized application and captures its standard output.
   - Parses the output to extract *only* the lower and upper bounds of the confidence interval (format: `lower,upper`).
   - Writes this exact string (e.g., `45.2,50.1`) to `/home/user/ci_result.txt`.

Constraints:
- Do not change the random seed or the number of bootstrap iterations (10,000).
- The output in `/home/user/ci_result.txt` must contain exactly the two float values separated by a comma.
- Ensure your bash script has executable permissions (`chmod +x`).