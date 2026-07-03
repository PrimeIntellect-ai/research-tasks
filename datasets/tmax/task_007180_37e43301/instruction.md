A data analyst on our team wrote a Go program, `/home/user/analyze.go`, to evaluate the results of a recent A/B test. The program is supposed to process two large data files:
1. `/home/user/users.csv` - Contains `user_id` and `group` (either 'A' or 'B').
2. `/home/user/sessions.csv` - Contains `user_id` and `duration` (a float representing session length in seconds).

The program needs to join these two data sources on `user_id` and calculate the difference in mean session durations between Group B and Group A (Difference = Mean(B) - Mean(A)), along with the 95% confidence interval for this difference. Because the dataset is large, we are using the standard normal distribution (Z-score = 1.96) for the unpooled two-sample confidence interval.

However, the analyst reported that the Go program currently outputs `NaN` or `0` for all statistics, similar to a plotting tool rendering a blank image due to a silent backend failure. They suspect there is a data cleanliness issue preventing the join from working correctly (e.g., inconsistent whitespace in the `user_id` fields).

Your task:
1. Identify and fix the data joining issue in the Go program (or rewrite it entirely using standard library packages like `encoding/csv`, `math`, and `encoding/json`). Ensure you strip any leading or trailing whitespace from the `user_id` before joining.
2. Calculate the sample mean and sample variance for both groups.
3. Compute the difference in means (Mean B - Mean A).
4. Compute the 95% Confidence Interval for the difference. The formula for the standard error of the difference is `sqrt((varA / nA) + (varB / nB))`. The CI bounds are `diff ± (1.96 * SE)`. Use $n-1$ for the sample variance calculation.
5. Save the final results to `/home/user/results.json` in the following exact format (numbers rounded to 4 decimal places):
```json
{
  "diff_means": 1.2345,
  "ci_lower": 0.1234,
  "ci_upper": 2.3456
}
```

Do not use any external Go statistical libraries (e.g., gonum); use only the Go standard library. You may run the script using `go run /home/user/analyze.go`.