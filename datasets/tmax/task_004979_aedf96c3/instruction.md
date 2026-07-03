You are a performance engineer analyzing a simulated server's CPU load profile. You need to build a reproducible data processing pipeline in Go that models the CPU utilization over time, calculates the total processing energy (integration), and measures the load volatility (differentiation) at a critical timestamp.

The CPU utilization percentage over time `t` (in seconds) is modeled by the function:
`f(t) = 50 + 20 * sin(0.1 * t) + 5 * cos(0.5 * t)`

Your task is to:
1. Write a Go program at `/home/user/profiler.go` that does the following:
   - Takes a single integer command-line argument to use as a random seed.
   - Computes the estimated total load (the integral of `f(t)` from `t = 0` to `t = 100`) using a **Monte Carlo integration** approach (the mean-value method: Area = width * average_height). Use exactly `N = 1,000,000` random uniform samples of `t` in the range `[0, 100]`. Use `math/rand` initialized with the provided seed.
   - Computes the numerical derivative of `f(t)` (load volatility) at exactly `t = 50` using the central difference method with a step size of `h = 0.001`. Formula: `(f(t+h) - f(t-h)) / (2*h)`.
   - Writes the results to a JSON file at `/home/user/profile_results.json` with the structure:
     ```json
     {
       "integral": 1234.56,
       "derivative": 12.34
     }
     ```
     *(Round values to 4 decimal places before writing to JSON, e.g., using `fmt.Sprintf("%.4f", val)` then converting back to float).*

2. Create a reproducible shell script at `/home/user/run_pipeline.sh` that:
   - Has executable permissions.
   - Compiles `/home/user/profiler.go`.
   - Runs the resulting binary, passing `12345` as the random seed.

Please implement the Go program and the pipeline script, and execute the pipeline script to generate the final JSON output.