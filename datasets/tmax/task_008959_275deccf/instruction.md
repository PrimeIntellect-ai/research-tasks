You are a Data Scientist tasked with cleaning a dataset and extracting statistical metrics using Go.

You have been provided with a dataset located at `/home/user/raw_data.csv`. The dataset represents paired sensor readings, but it is messy and contains malformed rows. 

Your task is to write a Go program to clean this data, enforce its schema, and calculate specific statistical metrics using the `gonum.org/v1/gonum/stat` library.

**Requirements:**

1. **Schema Enforcement & Cleaning:**
   - Read `/home/user/raw_data.csv`. The expected CSV header is `id,val_x,val_y`.
   - Enforce the following schema strictly: `id` must be an integer, `val_x` must be a float64, and `val_y` must be a float64.
   - Any row that contains empty fields, non-numeric strings (e.g., "NA", "error"), or fails to parse according to the schema must be dropped entirely.
   - Save the cleaned dataset to `/home/user/clean_data.csv`, preserving the original header and outputting the valid rows. Format the floats using standard formatting (e.g., `%v` or `%f` with appropriate precision so they match standard float representation without trailing zeros where unnecessary).

2. **Statistical Analysis:**
   - Use the cleaned data to calculate the following metrics:
     - The **Pearson correlation coefficient** between `val_x` and `val_y` (using `gonum/stat`).
     - The **Sample Mean** of `val_x`.
     - The **95% Confidence Interval** for the mean of `val_x`. Calculate the bounds using the formula: $Mean \pm 1.96 \times \frac{Sample StdDev}{\sqrt{N}}$, where $N$ is the number of valid rows and Sample StdDev is the standard deviation using Bessel's correction ($N-1$).

3. **Output format:**
   - Output the statistical results to a JSON file located at `/home/user/metrics.json`.
   - The JSON file must have exactly these keys: `"correlation"`, `"mean_x"`, `"ci_lower_x"`, and `"ci_upper_x"`.
   - Round the values in the JSON to exactly 4 decimal places.

**Constraints:**
- You must write the solution in Go.
- Use the standard `encoding/csv`, `encoding/json`, and `gonum.org/v1/gonum/stat` libraries.
- Initialize your Go module in `/home/user/sensor_project` (you will need to create this directory, run `go mod init`, and fetch dependencies).