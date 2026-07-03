You are a developer tasked with debugging a failing build in a Rust project. 

In your workspace at `/home/user/kepler_solver`, there is a Rust library that solves Kepler's equation ($E - e \sin(E) = M$) for orbital mechanics using the Newton-Raphson method. 

Recently, the CI pipeline has started experiencing intermittent failures. A test that runs various pairs of eccentricity (`e`) and mean anomaly (`M`) occasionally panics with a "Convergence failure". Upon initial inspection, the failure seems to happen for highly elliptical orbits (high eccentricity `e`).

Your task:
1. Run the test suite to reproduce the intermittent convergence failure.
2. Isolate the mathematical error in the Newton-Raphson formula implementation in `src/lib.rs`. (Hint: check the derivative calculation used for the update step).
3. Fix the formula implementation so that the algorithm correctly converges and all tests pass.
4. Verify your fix by running `cargo test`.
5. Create a file exactly at `/home/user/debugging_summary.txt` with exactly three lines:
   - Line 1: The exact buggy line of code in `src/lib.rs` (exactly as it originally appeared, with leading/trailing whitespace trimmed).
   - Line 2: Your corrected line of code (trimmed of leading/trailing whitespace).
   - Line 3: The exact text `ALL TESTS PASSED`.

Make sure you do not alter the test cases or the function signature, only the internal mathematical logic causing the divergence.