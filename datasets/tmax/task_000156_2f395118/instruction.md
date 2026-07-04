You have inherited an unfamiliar and broken Rust codebase located at `/home/user/math_service`. It is an HTTP service meant to replace an old legacy mathematical calculation engine. 

The old engine is a compiled, stripped executable located at `/app/legacy_calc`. This binary calculates the Nth term of a specific recurring mathematical sequence (a linear congruential sequence) based on secret internal constants (a seed, a multiplier, an increment, and a prime modulo). 

Your tasks are as follows:

1. **Extract the Constants**: Analyze the stripped binary at `/app/legacy_calc` to find the secret sequence parameters. The developer who wrote it left debug strings in the binary's memory/data sections in the format `[SECRET_CONFIG] ...`. You will need to extract these strings to know the correct mathematical formula.
2. **Repair the Environment**: The Rust codebase in `/home/user/math_service` is misconfigured. It fails to compile due to dependency version mismatches and edition errors in `Cargo.toml`. Furthermore, it tries to bind to port 80 (requiring root) and crashes. Fix the codebase so it compiles and listens on `0.0.0.0:8080`.
3. **Implement the Logic**: Fix the `calculate_sequence(n: u64)` function in the Rust codebase to compute the exact same Nth term as the legacy binary, using the extracted mathematical constants. Note: N=0 should return the initial seed. N=1 applies the formula once, etc.
4. **Construct a Regression Test**: Write a script at `/home/user/regression_test.py` that takes no arguments. It must loop through N from 0 to 50, executing `/app/legacy_calc N` and making an HTTP GET request to `http://127.0.0.1:8080/calc?n=N` on your running Rust service. The script must assert that the outputs match exactly.
5. **Start the Service**: Leave your fixed Rust HTTP service running in the background on port 8080.

The service must respond to HTTP GET requests at `/calc?n={N}` with an exact JSON payload: `{"result": <calculated_value>}`.

Do not ask for further assistance; implement the fixes, run the tests, and start the final service.