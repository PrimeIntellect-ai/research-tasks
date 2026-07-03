You are a data engineer debugging an ETL pipeline. We have a simple linear model used to score records, but the current bash-based pipeline is failing reproducibility tests. It silently outputs empty fields or incorrectly coerces types when encountering missing data, and it hardcodes the model weights instead of loading them dynamically.

Your task is to fix the pipeline script located at `/home/user/etl.sh` using standard Bash tools (like `awk`, `sed`, `grep`, `bash`). 

Here are the requirements for the fixed `/home/user/etl.sh`:
1. **Model Architecture Reconstruction**: Read the 3x1 weight vector (floats) from `/home/user/weights.txt`.
2. **Inference / Linear Algebra**: For each record in `/home/user/data.csv` (header: `id,f1,f2,f3`), compute the dot product of the feature vector `[f1, f2, f3]` and the weight vector.
3. **Data Imputation**: If any feature value (`f1`, `f2`, or `f3`) is completely empty (missing), impute it with `0` before multiplication. 
4. **Type Casting**: The dot product will result in a floating-point number. You must truncate this score to an integer (e.g., discarding the fractional part, equivalent to standard `int()` casting) to avoid silent float conversion downstream.
5. **Output**: Write the results to `/home/user/output.csv` with the exact header `id,score`. Subsequent rows should contain the integer `id` and the calculated integer `score`.

The script `/home/user/etl.sh` must be executable and perform all these steps when run without any arguments. The output file `/home/user/output.csv` must exactly match the expected integer scores.