You have inherited an unfamiliar and incomplete Go project from a former developer. You are provided with the following files in your home directory (`/home/user/`):

1. `simulator.go`: The source code for a chaos theory simulation calculating 10,000 iterations of the logistic map.
2. `old_sim`: A legacy, unstripped compiled binary of an older version of the simulator.

Currently, `simulator.go` is broken in several ways:
- **Build/Linker Error**: The code declares `func getSeed() float64` but lacks an implementation, causing a build failure.
- **Missing Knowledge**: The simulation requires a highly specific initial seed value to produce correct results. This seed was hardcoded as a package-level global variable named `main.Seed` in the legacy `old_sim` binary. Running `old_sim` does not print this value, so you must use a debugger (like `gdb`) or reverse engineering tools to inspect the binary and extract the value of `main.Seed`.
- **Numerical Instability**: The math in `simulator.go` is implemented using single-precision floats (`float32`). Because the logistic map is chaotic, using `float32` leads to rapid precision loss and catastrophic divergence from the true mathematical sequence. 

Your objectives are:
1. Extract the original float64 seed value from the `main.Seed` variable inside the `old_sim` binary.
2. Implement the missing `getSeed() float64` function in `simulator.go` so it returns the extracted seed value, fixing the build error.
3. Fix the numerical instability in `simulator.go` by upgrading all relevant variables and mathematical operations to use double-precision (`float64`).
4. Run the corrected Go program.
5. Save the final calculated value of the 10,000th iteration to `/home/user/result.txt`. The output must be formatted to exactly 6 decimal places (e.g., `0.123456`).

Do not change the number of iterations or the growth rate constant (`3.95`) present in the source code.