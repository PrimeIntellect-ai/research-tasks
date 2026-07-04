You are a researcher who needs to organize and analyze experimental dataset files using only shell scripting. You have two datasets collected from a mechanical experiment involving various springs:
- `/home/user/data/measurements.csv` (columns: `id`, `spring_id`, `displacement`)
- `/home/user/data/forces.csv` (columns: `id`, `force`)

Your task is to write a Bash script at `/home/user/analyze.sh` that performs the following steps:
1. **Data Schema Enforcement**: Check that `measurements.csv` exactly matches the header `id,spring_id,displacement` and `forces.csv` matches `id,force`. If either does not match, the script should exit with status code 1.
2. **Multi-source Data Joining**: Join the two CSV files on the `id` column.
3. **Model Training and Evaluation**: For each unique `spring_id`, fit a simple linear regression model with no intercept to find the spring constant $k$. The formula for the slope with no intercept is $k = \frac{\sum (x \cdot y)}{\sum (x^2)}$, where $x$ is `displacement` and $y$ is `force`.
4. **Experiment Tracking**: 
   - Write the results to `/home/user/results.csv` with the exact header `spring_id,k,num_samples`. Round $k$ to exactly two decimal places. The rows should be sorted alphabetically by `spring_id`.
   - Identify any spring where $k > 50$ and append its `spring_id` to `/home/user/stiff_springs.txt` (one per line, sorted alphabetically).

Make sure your script `/home/user/analyze.sh` is executable and run it to produce the final output files. Do not use Python or R for this; rely entirely on Bash and standard Unix text processing utilities (like `awk`, `join`, `sort`, `sed`).