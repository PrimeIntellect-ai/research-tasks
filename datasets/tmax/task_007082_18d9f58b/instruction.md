You are a data scientist analyzing spatial scientific data. You have a 2D mesh of temperature readings in a file at `/home/user/data/mesh.csv`. The mesh is a 100x100 grid of float values, where each row is a line in the CSV, and columns are comma-separated.

Your goal is to perform a statistical hypothesis comparison to check if there is a significant difference in temperature between specific regions of the domain. You must implement a reproducible computing pipeline using Go.

Please perform the following steps:
1. Write a Go program at `/home/user/pipeline/process_mesh.go`.
2. The program must read the `/home/user/data/mesh.csv` file.
3. Perform domain decomposition by splitting the 100x100 grid into four equal 50x50 quadrants:
   - Q1: Top-Left (rows 0-49, cols 0-49)
   - Q2: Top-Right (rows 0-49, cols 50-99)
   - Q3: Bottom-Left (rows 50-99, cols 0-49)
   - Q4: Bottom-Right (rows 50-99, cols 50-99)
4. Use Go goroutines to concurrently compute the sample mean and the unbiased sample variance for Quadrant 1 (Q1) and Quadrant 4 (Q4).
5. Compute the Welch's t-test statistic (`t_stat`) and the degrees of freedom (`df`) comparing Q1 and Q4. Test the null hypothesis that Q1 and Q4 have identical population means.
   - Formula for Welch's t-statistic: `t = (mean_q1 - mean_q4) / sqrt(var_q1/n1 + var_q4/n4)`
   - Formula for degrees of freedom: `df = (var_q1/n1 + var_q4/n4)^2 / ( (var_q1/n1)^2/(n1-1) + (var_q4/n4)^2/(n4-1) )`
6. The Go program should save the calculated statistics to `/home/user/pipeline/output.json` in the following exact JSON format:
```json
{
  "mean_q1": <float>,
  "mean_q4": <float>,
  "var_q1": <float>,
  "var_q4": <float>,
  "t_stat": <float>,
  "df": <float>
}
```

Constraints:
- Do not use external Go libraries for the math; write the calculations yourself using the standard library.
- Make sure to create the `/home/user/pipeline` directory.
- Compile and run your Go program so that `output.json` is generated.