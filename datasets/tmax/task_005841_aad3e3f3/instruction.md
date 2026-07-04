You are helping a researcher who is dealing with non-reproducible simulation results. 

The researcher has 20 simulation output datasets located in `/home/user/sim_runs/`. Each directory (named `run_1` to `run_20`) contains a file called `output.dat`, which holds a list of floating-point numbers (one per line). Due to the multi-threaded nature of the simulation dumps, the order of the numbers in these files is completely randomized.

When the researcher sums these numbers using a naive loop, the results vary wildly due to catastrophic cancellation and floating-point reduction order variations (the files contain extremely large numbers of opposite signs, alongside much smaller numbers).

The researcher has a reference dataset, `/home/user/reference.csv`, which contains the mathematically exact expected sum for each run in the format `run_id,expected_sum` (e.g., `run_1,42.5`).

Your task is to build a reproducible computation pipeline that correctly processes these outputs and compares them to the reference. 

Specifically, you must:
1. Create a bash script (or a script in Python/Awk invoked from bash) to read the `output.dat` for each of the 20 runs.
2. Sum the floating-point numbers in a way that eliminates floating-point precision loss and reduction order dependency (hint: consider standard libraries designed for exact floating-point summation).
3. Compare your computed sum to the `expected_sum` from `/home/user/reference.csv` by calculating the difference (`computed - expected`).
4. Perform a simple density categorization of the errors into three bins:
   - `exact`: difference is exactly `0.0`
   - `under`: difference is strictly less than `0.0`
   - `over`: difference is strictly greater than `0.0`
5. Save the final distribution counts to a JSON file at `/home/user/summary.json` with the following exact structure:
```json
{
  "distribution": {
    "exact": <count>,
    "under": <count>,
    "over": <count>
  }
}
```

Ensure your solution is robust and automatically creates `/home/user/summary.json` with the correct counts.