You are an MLOps engineer debugging a Go-based machine learning pipeline. 

We have a simple predictive modeling script in `/home/user/ml_pipeline/main.go` that performs dimensionality reduction (PCA via SVD) and a basic linear regression. It uses the `gonum.org/v1/gonum/mat` library.

Currently, the pipeline has a critical flaw: **Data Leakage**. The Principal Component Analysis (dimensionality reduction) is being fitted on the *entire* dataset before splitting it into training and testing sets. This means information from the test set leaks into the training process, leading to an artificially optimistic test Mean Squared Error (MSE).

Your task:
1. Run the existing `main.go` script and note the resulting Test MSE. (You may need to initialize the Go module and tidy the dependencies first).
2. Fix the data leakage in `/home/user/ml_pipeline/main.go`. Modify the pipeline so that:
   - The data is split into train and test sets *first*.
   - The column means and the PCA projection matrix (the principal components) are computed *only* using the training data.
   - Both the training and testing datasets are centered using the *training* means, and then projected into the reduced dimensional space using the *training* projection matrix.
3. Run the fixed script and note the new, corrected Test MSE (which should be slightly higher/different due to the removal of the leakage).
4. Create an experiment tracking file at `/home/user/experiment_results.json` with the following exact structure:
```json
{
  "leaky_mse": <float>,
  "strict_mse": <float>
}
```
Replace `<float>` with the exact numerical outputs printed by the program before and after your fix. Do not round the floats.

Ensure your modified Go program compiles and runs successfully.