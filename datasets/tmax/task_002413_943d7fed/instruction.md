You are a performance engineer analyzing a slow, diverging numerical simulation written in Go. The application models a non-linear chemical reaction using an adaptive step-size Ordinary Differential Equation (ODE) solver. However, the application frequently hangs or runs out of memory because the step-size adaptation logic is inverted, causing the solver to take infinitesimally small steps when the error increases, leading to a massive explosion in multi-dimensional state arrays.

Your task is to fix the ODE solver, reshape the output data, compute a probability distribution distance to verify correctness against observational data, and create a reproducible profiling pipeline.

Here are your specific objectives:

1. **Fix the Integrator:** 
   Look at the Go project in `/home/user/simulation`. The file `integrator.go` contains a custom adaptive Euler solver. Find the step-size adaptation logic. There is a bug where the new step size `dt` is multiplied by `(error / tolerance)` instead of `(tolerance / error)`. Fix this so the step size *decreases* when the error is high, and *increases* when the error is low. Ensure `dt` is clamped between `1e-6` and `0.1`.

2. **Reshape Observational Data:**
   The simulation currently outputs a flat 1D slice of floats representing interleaved time and state variables `[t0, y0, t1, y1, ...]`. Modify `main.go` to reshape this into a 2D array (slice of slices: `[][]float64`), where each inner slice is `[time, state]`. Write this reshaped data to `/home/user/simulation/output.csv` (comma-separated, no headers).

3. **Compute Distribution Distance:**
   There is a file `/home/user/simulation/observational_data.csv` containing the expected state distribution. Write a Go script (or add to `main.go`) to compute the 1-Wasserstein distance approximation between the sorted simulated states (the `y` values) and the sorted observational states. 
   *(Formula for this 1D approximation: mean absolute difference between the sorted arrays. Assume both arrays have the same length or truncate the longer one to match the shorter one's length).*
   Save the computed float value to `/home/user/simulation/metric.log`.

4. **Reproducible Profiling Pipeline:**
   Create a bash script at `/home/user/simulation/run_pipeline.sh` that:
   - Builds the Go application (`go build -o sim`).
   - Runs the application with CPU profiling enabled, saving the profile to `/home/user/simulation/cpu.prof`. (You must modify `main.go` to import `runtime/pprof` and start/stop the CPU profile).
   - Exits with a 0 status code if successful.

Ensure all file paths and names exactly match the instructions. You may install any standard Linux tools if needed.