You are acting as a research assistant for a physics lab. We need to simulate the energy spectrum of a hypothetical radiation source using a Monte Carlo method, process the simulated signal to find emission peaks, and automate the execution.

Please build a Go-based simulation and processing pipeline by following these exact specifications:

1. Environment Setup:
- Create a directory `/home/user/spectro_sim`.
- Initialize a Go module named `spectro_sim` in this directory.

2. Monte Carlo Simulation & Signal Processing (Go):
- Write a Go program `simulate.go` in the `/home/user/spectro_sim` directory.
- It must accept two command-line flags: `-seed` (integer, default 1) and `-samples` (integer, default 10000).
- Use `math/rand` with a local random generator (i.e., `rand.New(rand.NewSource(seed))`) to generate `samples` float64 energy values.
- For each sample, draw a random float64 `r` uniformly in [0.0, 1.0).
  * If `r < 0.7`: sample from a Uniform distribution over [0.0, 10.0).
  * If `0.7 <= r < 0.9`: sample from a Normal distribution with mean = 4.5 and standard deviation = 0.2.
  * If `r >= 0.9`: sample from a Normal distribution with mean = 7.5 and standard deviation = 0.1.
- Bin the generated values into a histogram with exactly 100 bins covering the range [0.0, 10.0). Bin `i` (from 0 to 99) corresponds to the interval `[i*0.1, (i+1)*0.1)`. Discard any values strictly outside [0.0, 10.0).
- Apply a 3-point moving average filter to the histogram counts to create a smoothed spectrum. The smoothed value for bin `i` is $S_i = (H_{i-1} + H_i + H_{i+1}) / 3.0$ (use float64 for $S_i$). Assume boundary counts $H_{-1} = 0$ and $H_{100} = 0$.
- Detect peaks in the smoothed spectrum. A bin `i` is a peak if its smoothed value $S_i$ is strictly greater than $S_{i-1}$ and strictly greater than $S_{i+1}$, AND $S_i > 100.0$. (Again, assume $S_{-1} = 0$ and $S_{100} = 0$).
- The program must write the detected peaks to `/home/user/spectro_sim/peaks.csv` with the exact header `BinIndex,BinCenter,SmoothedCount`. The `BinCenter` is calculated as `i*0.1 + 0.05`. Format floats to 3 decimal places.

3. Automation:
- Write a bash script `/home/user/spectro_sim/run_pipeline.sh` that:
  a. Compiles `simulate.go` into an executable named `simulator`.
  b. Runs the compiled executable with `-seed 12345` and `-samples 500000`.
  c. Parses `peaks.csv`, sorts the peaks by `SmoothedCount` in descending order, and extracts the `BinCenter` of the top 2 highest peaks.
  d. Writes these two `BinCenter` values (one per line, just the numbers) into `/home/user/spectro_sim/top_peaks.txt`.

Ensure the bash script is executable. Run the pipeline script yourself so the final `peaks.csv` and `top_peaks.txt` files are generated and available for verification.