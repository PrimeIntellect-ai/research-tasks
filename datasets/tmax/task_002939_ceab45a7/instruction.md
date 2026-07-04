You are a data scientist tasked with cleaning a noisy dataset of sensor readings using a statistical model. 

You have been provided with a CSV file at `/home/user/sensor_data.csv`. It has two columns, `X` and `Y`, representing a single feature and a target variable. Most of the data follows a linear relationship, but there are a few severe outliers caused by sensor malfunctions.

Your objective is to write a Go program to train a simple linear regression model, use it to identify and remove outliers, and benchmark its inference time.

Perform the following steps:
1. Create a Go module in `/home/user/sensor` (e.g., `go mod init sensor`).
2. Write a Go program at `/home/user/sensor/clean.go` that:
   - Reads `/home/user/sensor_data.csv`.
   - Fits a Simple Linear Regression model ($Y = mX + c$) to the entire dataset using Ordinary Least Squares (OLS) to minimize the sum of squared errors. Do not use any external machine learning libraries; implement the math directly.
   - Calculates the residual for each data point: $r_i = Y_i - (mX_i + c)$.
   - Calculates the population standard deviation ($\sigma$) of all the residuals (using division by $N$, not $N-1$).
   - Filters out any data points where the absolute residual is strictly greater than $2\sigma$ ($|r_i| > 2\sigma$).
   - Writes the remaining clean data points back to a new file at `/home/user/cleaned_data.csv` in the exact same format (with the `X,Y` header, keeping original precisions or formatting to 4 decimal places if regenerated, though original values are integers/simple floats).
3. Write a standard Go benchmark test in `/home/user/sensor/clean_test.go` named `BenchmarkInference`. The benchmark should measure the time it takes to compute a single prediction $Y = mX + c$ using the $m$ and $c$ learned from the noisy dataset, for an arbitrary input $X = 10.0$.
4. Run your benchmark and save the terminal output to `/home/user/benchmark.txt` (e.g., using `go test -bench=. > /home/user/benchmark.txt`).

**Constraints & Specifications:**
- Read and parse variables as `float64`.
- The OLS formulas are: 
  $m = \frac{N \sum(XY) - \sum X \sum Y}{N \sum(X^2) - (\sum X)^2}$
  $c = \frac{\sum Y - m \sum X}{N}$
- Write out the cleaned CSV with exactly the same header `X,Y`. Output the values formatted to exactly 1 decimal place (e.g., `5.0,19.5`).

Once you have produced `/home/user/cleaned_data.csv` and `/home/user/benchmark.txt`, the task is complete.