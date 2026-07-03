You are a data engineer tasked with building an automated ETL pipeline that computes posterior expectation scores for a set of observations. Due to strict legacy system constraints, your entire solution must be implemented using only Bash and standard POSIX CLI utilities (e.g., `awk`, `join`, `sed`, `bc`, `tesseract`). Do not use Python, R, or Perl for the data processing logic.

You are provided with three input artifacts:
1. `/app/table_a.tsv`: A tab-separated file containing the columns `ID`, `F1`, and `F2`.
2. `/app/table_b.csv`: A comma-separated file containing the columns `ID` and `F3`.
3. `/app/config_matrix.png`: An image of a configuration document containing Bayesian prior probabilities (`PRIOR_A`, `PRIOR_B`) and linear regression weights (`W1`, `W2`, `W3`).

Your task:
1. Extract the configuration parameters from the image (you may use `tesseract`).
2. Write a Bash script at `/home/user/etl_pipeline.sh` that processes the input data.
3. The script must join the two datasets on the `ID` column.
4. For each joined record, calculate the expected score using the following formula:
   `Score = PRIOR_A * (W1 * F1 + W2 * F2) + PRIOR_B * (W3 * F3)`
5. Run your script and save the output to `/home/user/results.csv`.
6. The output file `/home/user/results.csv` must be a comma-separated file with exactly two columns: `ID,Score`. The first row must be the header. The rows must be sorted by `ID` in ascending order.

Ensure your pipeline accurately parses the numerical values from the image and handles floating-point arithmetic correctly (e.g., via `awk` or `bc`).