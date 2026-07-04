I'm a data scientist building a lightweight, dependency-free pipeline. I need to compute analytical Ordinary Least Squares (OLS) regression parameters directly in Bash without relying on Python or R, to serve as a fast regression test for our more complex models.

Please write a Bash script at `/home/user/fit_model.sh` that reads a CSV file (provided as the first positional argument) with a header row `x,y` and computes the OLS slope (m) and intercept (b) using `awk` (to ensure 64-bit floating-point numerical precision).

The formulas for the analytical OLS solution are:
m = (N * sum(x*y) - sum(x)*sum(y)) / (N * sum(x^2) - (sum(x))^2)
b = (sum(y) - m * sum(x)) / N

Your script must:
1. Skip the header row.
2. Accumulate the necessary sums.
3. Compute `m` and `b`.
4. Print exactly: `m=<slope>,b=<intercept>` where both values are formatted to exactly 6 decimal places.

Once you have written the script, make it executable and run it on `/home/user/data.csv`. Save the standard output of this run to `/home/user/result.txt`.