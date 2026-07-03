You are a machine learning engineer preparing a new batch of training data for a predictive model.

You have a raw dataset located at `/home/user/data_prep/raw_data.csv`. The file contains a header `id,y,a,b`, followed by 100,000 rows of floating-point data. 
The feature our model needs is `x`, which is not directly provided. However, the variables follow the linear equation:
`a * x + b = y`

Your objective is to:
1. Solve for the feature `x` for every row in `raw_data.csv`. 
2. We have an existing verified dataset located at `/home/user/data_prep/reference.csv` (header: `id,x`). You need to compare your computed `x` values against this reference.
3. Identify all anomalies. An anomaly is defined as:
   - An `id` that exists in `raw_data.csv` but is completely missing from `reference.csv`.
   - An `id` where the absolute difference between your calculated `x` and the reference `x` is strictly greater than `0.01`.
4. Output the anomalous `id`s (just the integer IDs, one per line, sorted numerically in ascending order) to `/home/user/data_prep/anomalies.txt`.

**Performance constraint:**
Because the dataset is large (in a real-world scenario it would be terabytes), you must perform the row processing in parallel. You must write a bash script or command pipeline that splits the workload and uses standard Linux parallelization tools (such as `xargs -P`, GNU `parallel`, or backgrounding with `&` and `wait`) to utilize at least 4 parallel processes. You may write a short helper script in any language (like Python, awk, etc.) to perform the math/comparison, but the orchestration must demonstrate parallel execution.

Ensure the final `anomalies.txt` contains exactly the sorted integer IDs of the anomalous records.