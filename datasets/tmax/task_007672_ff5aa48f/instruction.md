You are a data engineer building a test suite for an ETL pipeline. A previous engineer left behind a data validation requirement, but the Python test script is missing. Similar to a visualization script that silently produces blank plots due to a backend misconfiguration, our current pipeline is failing silently because the data validation and model inference tests are bypassing schema checks and linear algebra operations.

Your task is to write a Python script at `/home/user/etl_test.py` that reads a dataset, enforces its schema, calculates the covariance matrix, and runs a simple linear inference step. 

You have been provided with two files:
1. `/home/user/data.csv` (contains raw pipeline data with headers `X`, `Y`, and `Label`)
2. `/home/user/weights.json` (contains a JSON array of two model weights for `X` and `Y`)

Your script must perform the following:
1. **Schema Enforcement**: Read `/home/user/data.csv`. Ensure column `X` is strictly treated as an integer and column `Y` as a float. Drop any rows that cannot be cast to these types, or are missing values (do not crash). Ignore the `Label` column for computations.
2. **Covariance Analysis**: Calculate the sample covariance matrix for the valid `X` and `Y` columns (a 2x2 matrix). Compute the trace (sum of the main diagonal) of this covariance matrix.
3. **Model Inference & Linear Algebra**: Reconstruct a simple linear model using the weights from `/home/user/weights.json`. The weights correspond to `[weight_X, weight_Y]`. Perform matrix multiplication (or equivalent linear algebra operations) to compute the predicted value for each valid row: `Prediction = X * weight_X + Y * weight_Y`. Calculate the mean of these predictions.
4. **Reporting**: Write the computed trace and mean prediction to `/home/user/results.txt` in the exact following format:
```
Trace: <value>
Mean_Prediction: <value>
```
Format both values to exactly two decimal places.

Ensure your script runs successfully and writes the correct values to `/home/user/results.txt`.