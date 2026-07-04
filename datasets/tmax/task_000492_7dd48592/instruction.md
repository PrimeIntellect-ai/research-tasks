You are assisting a computational astrophysicist in resolving a critical precision issue in a star cluster simulation. 

We have a proprietary, closed-source simulation engine located at `/app/cluster_sim` (it is a stripped binary). When executed, it outputs 5,000,000 lines of CSV data to stdout. Each line represents a particle in the format: `x,y,z,mass`. 

The researcher previously wrote a standard Go program to compute the Center of Mass (CoM) for these particles. However, because the system is highly unstable, it contains particles with massive positive and negative coordinate coordinates that nearly cancel each other out. The naive parallel summation they used caused non-reproducible results due to floating-point reduction order and catastrophic cancellation. 

Your task is to write a highly precise, parallel Go program at `/home/user/com.go` that does the following:
1. Executes `/app/cluster_sim` and streams its output.
2. Parses the CSV data (`x`, `y`, `z`, `mass` are all float64).
3. Computes the global Center of Mass (CoM_x, CoM_y, CoM_z) using a stable summation algorithm (e.g., Kahan summation or Neumaier summation) to mitigate floating-point accumulation errors. 
4. Uses goroutines to process the data in parallel chunks, but ensures the final reduction step combines the chunks deterministically and without losing the precision gained by your stable summation.
5. Performs a statistical bootstrap (using 1,000 resamples of the chunked partial sums) to compute the 95% confidence interval for the CoM coordinates, simulating the variance across spatial sub-regions.

Your Go program must output the final computed values to `/home/user/result.json` in the following exact format:
```json
{
  "CoM": {
    "x": 0.0000000000000,
    "y": 0.0000000000000,
    "z": 0.0000000000000
  },
  "ConfidenceInterval_95": {
    "x_lower": 0.0, "x_upper": 0.0,
    "y_lower": 0.0, "y_upper": 0.0,
    "z_lower": 0.0, "z_upper": 0.0
  }
}
```

Constraints & Notes:
- Standard naive summation `sum += value` will fail the precision check. You *must* implement a compensated summation algorithm.
- The evaluation will use a metric threshold: The Maximum Absolute Error (MAE) between your computed `CoM` coordinates and an exact arbitrary-precision reference must be less than `1e-10`.
- Do not store all 5,000,000 records in memory at once (stream it or chunk it), to avoid OOM issues.
- You can use standard library packages only.

Write and execute the Go code, ensure it produces the `result.json` file, and verify your logic.