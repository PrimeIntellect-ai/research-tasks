You are helping a researcher who is running numerical simulations of a heat transfer model. The researcher has a Python script `/home/user/heat_sim.py` that computes the total heat over a 2D domain. To simulate parallel processing, the domain is decomposed into chunks, and the sums are accumulated. However, the researcher noticed that changing the number of chunks changes the final result due to floating-point reduction order issues. 

Your tasks are as follows:
1. **Fix Floating-Point Order Issue**: Modify `/home/user/heat_sim.py`. Update the `compute_heat(N, num_chunks)` function so that instead of accumulating naively, it collects every individual cell's computed value into a flat list, and then returns the exact floating-point sum of that list using `math.fsum`. This ensures the result is perfectly reproducible and independent of `num_chunks` and domain decomposition order.

2. **Convergence Testing**: Create a script `/home/user/run_analysis.py` that imports `compute_heat` from `heat_sim`. Run the simulation for grid sizes $N \in \{10, 20, 40, 80, 160, 320\}$. Find the *first* $N$ (starting from 20) where the absolute difference between the result at $N$ and the result at $N/2$ is strictly less than $1 \times 10^{-6}$. This is your `converged_N`, and the result at this $N$ is `converged_value`.

3. **Observational Data Reshaping**: The researcher has observational data in `/home/user/obs_data.txt`. This file contains a single comma-separated line of floating-point temperature values. This data corresponds to a square 2D grid. Reshape this 1D data into a 2D numpy array (the grid size is the square root of the number of elements). Compute the exact sum of all these values using `math.fsum(data.flatten())`. This is your `obs_value`.

4. **Reporting**: Write the final results to `/home/user/final_report.json` with the exact following JSON structure:
```json
{
  "converged_N": 40,
  "converged_value": 0.123456789,
  "obs_value": 0.987654321
}
```
(Replace the numbers with the actual computed values).

Do not change the mathematical function inside `heat_sim.py`; only change how the values are accumulated and summed.