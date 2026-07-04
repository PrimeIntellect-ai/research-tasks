You are an MLOps engineer debugging a feature engineering pipeline written in C. 

The pipeline tracks experiment artifacts and attempts to find the most similar historical experiment (Reference) for each new experiment (Query) based on two extracted performance metrics: `cpu_time` and `memory_usage`.

To compute the similarity (Euclidean distance), the features are min-max scaled. However, there is a data leakage bug: the pipeline currently calculates the minimum and maximum values for scaling across the *entire* dataset (both Reference and Query sets) instead of fitting the scaler *only* on the Reference set.

**Your Tasks:**
1. Inspect the C source code located at `/home/user/pipeline.c`.
2. Identify and fix the data leakage bug so that the min-max scaling parameters (`min` and `max` for each feature) are computed **strictly using the Reference experiments** (the first `NUM_REF` rows). The scaling transformation should then be applied to all rows using those Reference-derived parameters.
3. Compile your fixed C code (e.g., `gcc -o pipeline pipeline.c -lm`).
4. Run the compiled executable. It will read `/home/user/experiments.csv` and should output the results to `/home/user/results.csv`.

**Data details:**
- `/home/user/experiments.csv` contains 10 rows: `ExperimentID, cpu_time, memory_usage`.
- The first 7 rows are historical "Reference" experiments.
- The last 3 rows are new "Query" experiments.

**Expected Output Format:**
The output file `/home/user/results.csv` must be written by your C program in the following format (which the provided C code already handles, you just need to fix the math/logic):
```
QueryID,ClosestReferenceID,Distance
8,X,Y.YYYY
...
```
(Distance should be printed to 4 decimal places).