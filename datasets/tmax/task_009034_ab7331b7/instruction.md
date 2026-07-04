You are helping a data scientist debug a biological network simulation. 

In `/home/user/workspace/`, there is a Go script named `simulate_network.go`. This script simulates a simple biochemical reaction (using Euler's method for an ODE: dy/dt = -k*y) across 1000 independent network nodes to estimate the mean final concentration (density).

Currently, the script uses goroutines to speed up the independent ODE simulations. However, it updates a shared floating-point variable `totalDensity` using a mutex lock. Because floating-point addition is not strictly associative and the goroutines complete in a non-deterministic order, the script produces slightly different results (at the 10th decimal place) on every run. This non-reproducibility is breaking our regression tests.

Your task is to fix `simulate_network.go` so that the output is strictly deterministic. 

Requirements:
1. Modify `simulate_network.go` to remove the concurrent mutex-based summation.
2. Collect the final concentrations (`yFinal`) into a slice (array) indexed such that index `0` corresponds to `id=1`, index `1` corresponds to `id=2`, etc.
3. After all goroutines complete, sum the slice sequentially from index `0` to `N-1` to calculate `totalDensity`.
4. Do not change the ODE parameters, the number of steps, or the initial conditions.
5. Once fixed, run the script 5 times and redirect all 5 outputs into a new file located at `/home/user/workspace/stable_output.txt`. The file should contain exactly 5 identical lines.