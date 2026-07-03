You are a scientific computing researcher tasked with porting a legacy C simulation to Python and performing regression and numerical stability testing.

The simulation models a particle in a non-linear potential over 1000 time steps for 10,000 independent trajectories, driven by pre-generated noise. The legacy C code `sim.c` has been provided in `/home/user/`.

Your objectives:

1. **Run the Baseline**: Compile and execute `/home/user/sim.c`. It reads 10,000,000 double-precision floats (IEEE 754) from `/home/user/noise.bin` and outputs the final positions of the 10,000 trajectories to `/home/user/baseline.txt`.

2. **Implement Python Port**: Write a Python script that exactly replicates this simulation. You must produce two new sets of results:
   - **Float64**: Perform the simulation using 64-bit floating point precision (read noise as `np.float64`, initialize states as `np.float64`). Save the final positions to `/home/user/py_float64.txt` (one per line).
   - **Float32**: Perform the simulation using 32-bit floating point precision (cast noise to `np.float32`, initialize states as `np.float32`). Save the final positions to `/home/user/py_float32.txt`.
   *(Hint: You may vectorize the simulation across trajectories in NumPy to speed it up, provided the mathematical operations remain identical).*

3. **Statistical Comparison**: Write a script to compare the distributions of the final positions. Using `scipy.stats`, calculate the 1D Wasserstein distance (`wasserstein_distance`) and the Kolmogorov-Smirnov statistic (`ks_2samp().statistic`) between the baseline and your Python implementations.

4. **Output Metrics**: Create a JSON file at `/home/user/metrics.json` containing the calculated metrics exactly matching this format:
```json
{
  "ks_stat_float32": <float>,
  "ks_stat_float64": <float>,
  "wd_float32": <float>,
  "wd_float64": <float>
}
```
All keys must be present and values must be floats.

Ensure all file paths are strictly observed.