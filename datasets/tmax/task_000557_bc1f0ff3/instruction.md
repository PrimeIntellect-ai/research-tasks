You are a Machine Learning Engineer responsible for building a data preparation service. We need a backend service that processes incoming raw datasets, enforces a strict data schema, calculates confidence intervals to check for data drift, and determines if the dataset is ready for our regression models.

Your task is to build and run a Go HTTP server that serves this data preparation pipeline. 

Here are the requirements:

1. **Vendored Library Fix:** 
   We have pre-vendored a custom statistics library at `/app/vendored/statslib`. It is required for calculating confidence intervals. However, the package is currently broken. To make it usable, you need to generate its look-up tables. Inside `/app/vendored/statslib`, there is a `Makefile` that runs a python script (`gen.py`) to generate `tables.go`. The script fails because it expects a specific environment variable to be set. Figure out what the environment variable is, fix the generation step, and ensure the Go package compiles.

2. **Go Environment Setup:**
   Create a new Go module at `/home/user/ml-api` (module name `ml-api`). 
   Ensure it can import the fixed statslib using the import path `github.com/local/statslib` by adding the appropriate `replace` directive in your `go.mod` pointing to `/app/vendored/statslib`.

3. **Data Preparation API:**
   Write a Go HTTP server in `/home/user/ml-api/main.go` that listens on `127.0.0.1:8080`.
   It must expose a single endpoint:
   - **Method:** `POST`
   - **Path:** `/api/v1/prepare`
   - **Auth:** Require an HTTP header `Authorization: Bearer train-token-99`
   - **Input:** A JSON payload with a single field `data`, which is an array of objects representing rows. E.g., `{"data": [{"feature_1": 1.5, "feature_2": 2.0, "target": 10.5}, ...]}`

4. **Pipeline Logic:**
   When a request is received, the server should process the `data` array as follows:
   - **Schema Enforcement:** Verify that every object in the data array contains exactly the keys `"feature_1"`, `"feature_2"`, and `"target"`, and that all values are numeric (float64). If any row violates this, return an HTTP 400 response with `{"error": "invalid schema"}`.
   - **Confidence Interval (Hypothesis Testing):** Extract all values for `feature_1` into a `[]float64` slice. Use the `github.com/local/statslib` function `statslib.CalculateCI(data []float64)` to compute the lower and upper bounds of the 95% confidence interval for `feature_1`.
   - **Regression Readiness:** The dataset is considered ready for regression if the confidence interval lower bound is strictly greater than 0.0, and the upper bound is strictly less than 100.0.
   - **Output:** Return an HTTP 200 JSON response in this exact format:
     ```json
     {
       "schema_valid": true,
       "ci_lower": <float>,
       "ci_upper": <float>,
       "regression_ready": <boolean>
     }
     ```

Compile your code, start the server in the background, and ensure it is listening on `127.0.0.1:8080`.