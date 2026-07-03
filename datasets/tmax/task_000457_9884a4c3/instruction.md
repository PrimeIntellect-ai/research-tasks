We are conducting high-volume integration testing for a new web API, but our security token validation component is causing severe bottlenecks. The API relies on a proprietary token validator provided as a stripped Linux executable at `/app/api_oracle`.

Every time we test an API endpoint in our suite, the test harness calls `/app/api_oracle <token>`. Unfortunately, the overhead of forking this process millions of times is unacceptable. 

Your task is to:
1. Reverse-engineer the stripped binary `/app/api_oracle` to understand the mathematical constraints it uses to validate a token. (It takes a single token as an argument and returns exit code 0 if valid, 1 if invalid).
2. Create a minimal, highly optimized Rust replacement binary at `/home/user/fast_validator`. It must read a file containing newline-separated tokens, evaluate each token using the exact same constraints as the oracle, and print only the valid tokens to standard output.
3. Configure the build system (using `rustc` or `cargo`) to compile this binary with maximum optimizations.

We have provided a sample of 1,000,000 generated test tokens at `/home/user/tokens.txt`. 
You must output the valid tokens to `/home/user/valid.txt` by running:
`/home/user/fast_validator /home/user/tokens.txt > /home/user/valid.txt`

The goal is extreme performance. An automated verifier will measure the execution time of your `/home/user/fast_validator` against a baseline script that simply invokes `/app/api_oracle` in a loop. You must achieve a massive speedup threshold for the build to pass.