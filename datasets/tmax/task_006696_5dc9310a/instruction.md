You are a Machine Learning Engineer preparing a dataset for a new model. You have a raw dataset located at `/home/user/raw_data.csv` which contains some messy data. 

Your task is to write a Go program that processes this data, enforces a strict schema, performs precise numerical scaling, and splits the data into reproducible training and validation sets.

Here are the step-by-step requirements:

1. **Setup**:
   - Create your Go project in `/home/user/ml_prep/`.
   - Initialize a Go module named `ml_prep`.
   - You must use the `gonum.org/v1/gonum/stat` package to calculate the mean and standard deviation (do not implement these from scratch).

2. **Data Schema Enforcement**:
   - Read `/home/user/raw_data.csv`. The expected CSV header is: `id,feature_a,feature_b,category`.
   - Validate each row. A valid row must:
     - Have an `id` that parses to an integer.
     - Have `feature_a` and `feature_b` that parse to `float64`.
     - Have exactly 4 columns.
   - If a row is invalid, discard it. Append the raw string value of the `id` column (or whatever was in the first column of the bad row) to a log file at `/home/user/discarded.log` (one per line).

3. **Numerical Transformation**:
   - For all *valid* rows, compute the population mean and population standard deviation of `feature_a` and `feature_b` using the `gonum` package (use the valid dataset as the entire population, weights = nil).
   - Apply Z-score standardization to `feature_a` and `feature_b`: `z = (x - mean) / stddev`.
   - Format the new standardized values to exactly 6 decimal places (e.g., `fmt.Sprintf("%.6f", val)`).

4. **Reproducible Pipeline Splitting**:
   - Your compiled program must accept a command-line flag `-seed` (an integer).
   - Use `math/rand` seeded with this value to randomly shuffle the valid, standardized rows.
   - Split the shuffled rows: the first 50% go to `/home/user/ml_prep/train.csv` and the remaining 50% go to `/home/user/ml_prep/val.csv`. (If the number of valid rows is odd, `train.csv` gets the extra row, i.e., `ceil(N/2)`).
   - The output CSVs must include the header `id,feature_a,feature_b,category`.

5. **Execution**:
   - Build your tool and run it with the flag `-seed=42`.
   - Ensure `train.csv`, `val.csv`, and `discarded.log` are generated properly.

Your final code should be a completely working Go application in `/home/user/ml_prep/main.go`. Leave the output files in their specified locations for verification.