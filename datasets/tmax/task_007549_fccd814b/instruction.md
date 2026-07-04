You are an AI assistant helping a data scientist preprocess an observational dataset before feeding it into a spatial matrix factorization model. The model tends to crash when fed "near-singular" inputs (which in this context means spatial regions with zero or near-zero variance).

You have been given two files in the `/home/user/` directory:
1. `observations.csv`: The raw observational data collected on a 10x10 spatial grid. The columns are `x,y,value`.
2. `reference.csv`: A trusted reference dataset on the same 10x10 grid. The columns are `x,y,value`.

Your task is to write a purely Bash-based pipeline (using standard utilities like `awk`, `sed`, `grep`, `sort`, `join`, `bc`, etc. - NO Python/R allowed) to perform domain decomposition, filtering, and comparison.

Follow these specific steps:
1. **Domain Decomposition:** Conceptually split the 10x10 grid (where x and y range from 0 to 9) into four 5x5 quadrants:
   - Q1: x in [0,4], y in [0,4]
   - Q2: x in [5,9], y in [0,4]
   - Q3: x in [0,4], y in [5,9]
   - Q4: x in [5,9], y in [5,9]

2. **Singularity Check:** For each quadrant in `observations.csv`, calculate the population variance of the `value` column. If the variance is strictly less than `0.1`, the quadrant is considered "near-singular" and must be flagged as `Singular`. 
   *(Note: Population variance = sum(x^2)/N - (sum(x)/N)^2)*

3. **Reference Comparison:** For the remaining non-singular quadrants, compare the `observations.csv` values to the `reference.csv` values cell-by-cell. Calculate the Mean Absolute Error (MAE) for the quadrant. If the MAE is strictly greater than `5.0`, flag the quadrant as `Anomalous`. Otherwise, flag it as `Valid`.

4. **Output Generation:** Write the final classifications to `/home/user/model_inputs.log`. The file must contain exactly four lines, formatted exactly like this, sorted by quadrant:
   ```
   Q1: [Status]
   Q2: [Status]
   Q3: [Status]
   Q4: [Status]
   ```
   Replace `[Status]` with `Singular`, `Anomalous`, or `Valid` based on your calculations.

Ensure your script handles floating-point operations carefully (e.g., via `awk` or `bc`).