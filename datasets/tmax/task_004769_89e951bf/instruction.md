You are an AI assistant helping a biomedical researcher organize and analyze an intricate multi-omics dataset. 

You need to process two raw datasets, perform statistical analyses, and expose the results via a local HTTP API. However, a crucial custom data processing library the lab uses is currently broken and needs fixing before you can proceed.

**Step 1: Fix and Install the Vendored Package**
There is a custom Python package called `labschema` pre-vendored at `/app/labschema-1.2.0`. It is used for strict schema enforcement. 
The package's `Makefile` has a perturbation that prevents it from installing correctly (a typo in the `install` target). 
Fix the `Makefile` and install the package into the current Python environment (using `make install`).

**Step 2: Data Cleaning and Joining**
You have two datasets:
1. `/home/user/data/clinical.csv`: Contains `patient_id` (string), `age` (integer), and `recovery_time` (float).
2. `/home/user/data/biomarkers.json`: Contains a list of JSON objects with `patient_id` (string) and 10 numerical biomarker readings (`marker_1` to `marker_10`).

Using the `labschema` library, you must filter both datasets. Any row/object that does not have the exact correct data types should be discarded (assume the library provides a `labschema.validate_clinical(dict)` and `labschema.validate_biomarkers(dict)` which raise `labschema.ValidationError` on failure).
Join the cleaned datasets on `patient_id` via an inner join.

**Step 3: Dimensionality Reduction and Hypothesis Testing**
1. Extract the 10 biomarker features (`marker_1` through `marker_10`) from the joined dataset.
2. Standardize the biomarker features (mean=0, variance=1).
3. Perform Principal Component Analysis (PCA) to reduce the 10 biomarkers to 2 principal components (PC1 and PC2).
4. Calculate the Pearson correlation coefficient between PC1 and `recovery_time`, along with the associated p-value (to test the hypothesis that PC1 is correlated with recovery time).

**Step 4: Expose the Results via an HTTP API**
Write a Python script (e.g., using `Flask` or `FastAPI`) that serves an HTTP API with the following specifications:
- **Host:Port**: Listen strictly on `127.0.0.1:8080`.
- **Authentication**: All endpoints must require an `Authorization: Bearer LAB_SECURE_TOKEN_99` header. Return a 401 status code if missing or invalid.
- **Endpoint 1 (`GET /api/pca`)**: 
  Returns a JSON object containing the explained variance ratios of the two principal components:
  `{"explained_variance_ratio": [val1, val2]}`
- **Endpoint 2 (`GET /api/stats`)**:
  Returns a JSON object with the correlation and p-value from your hypothesis test:
  `{"pc1_recovery_corr": <float>, "p_value": <float>}`

Leave the server running in the background so it can be queried by the verification suite.