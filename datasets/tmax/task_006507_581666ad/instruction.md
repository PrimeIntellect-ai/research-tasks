You are an operations engineer triaging an incident. Customers of our Go-based financial service have reported that their annualized yield calculations are drifting by small amounts, resulting in incorrect payouts. 

The source code for the calculation engine is located in a Git repository at `/home/user/finance-api`. 

Customer support has provided a test case that used to work perfectly:
- **Principal**: 1000000.0
- **Daily Rate**: 0.00015
- **Days**: 365
- **Expected Yield**: `1056272.541315516`

Currently, on the `main` branch, this calculation is returning a different value due to a precision loss bug introduced in a recent commit. We know the code was working correctly at the `v1.0.0` tag.

Your task is to:
1. Construct a Go regression test or script that executes `CalculateYield(1000000.0, 0.00015, 365)` from the `finance` package and asserts that the value matches the expected yield (with a tolerance of `0.000001`).
2. Use `git bisect` in combination with your regression test to isolate the exact commit that introduced the precision loss.
3. Calculate the exact absolute difference (drift) between the correct expected yield (`1056272.541315516`) and the incorrect actual yield produced by the buggy commit.
4. Output your findings into a JSON file located at `/home/user/resolution.json` with the following exact structure:

```json
{
  "bad_commit": "<full_git_commit_hash>",
  "drift_amount": <absolute_difference_as_float_rounded_to_3_decimal_places>
}
```

Constraints:
- You must use Go to compile and run the test against the repository's code.
- Round the `"drift_amount"` to exactly 3 decimal places (e.g., `9.621`). 
- Do not modify the repository's historical commits; only inspect them and identify the culprit.