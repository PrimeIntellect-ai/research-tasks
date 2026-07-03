You are a data engineer building an ETL pipeline to process incoming sensor feature vectors before they are loaded into a database. The data is received as a CSV file, but it contains missing values, potential anomalies, and requires basic linear algebra transformations.

Write a Bash script (e.g., using `awk`, `bash`, or standard GNU utilities) located at `/home/user/process_etl.sh` that processes an incoming CSV file located at `/home/user/incoming_data.csv`. 

The input CSV has the following header:
`id,v1,v2,v3,v4`

Your script must perform the following steps:
1. **Missing Value Handling**: Read the input file. Any empty fields in the `v1`, `v2`, `v3`, or `v4` columns must be imputed with the value `0.0`.
2. **Linear Algebra Operations**: For each row's vector `V = [v1, v2, v3, v4]`:
   - Compute the L2 norm (Euclidean length) of the vector.
   - Compute the dot product of the vector `V` with a fixed weight vector `W = [0.5, -0.5, 1.0, 2.0]`.
3. **Outlier Detection**: If the L2 norm of the vector is strictly greater than `10.0000`, flag the row as an outlier (value `1`), otherwise `0`.
4. **Numerical Formatting**: Ensure your script's numerical output correctly formats all floating-point numbers to exactly 4 decimal places (e.g., `10.5000`, `3.1623`).
5. **Output Generation**: Write the results to a new CSV file at `/home/user/processed_data.csv`. 

The output CSV must have the following header:
`id,v1,v2,v3,v4,l2_norm,dot_product,is_outlier`

Requirements:
- Ensure `/home/user/process_etl.sh` is executable (`chmod +x`).
- Running `/home/user/process_etl.sh` should read `/home/user/incoming_data.csv` and create `/home/user/processed_data.csv`.
- Use standard Linux command-line tools (Bash, awk, sed, bc, etc.) to accomplish this without relying on external python/R scripts.