You are a data scientist cleaning up model outputs to test pipeline reproducibility. We have two datasets representing the output of a machine learning inference pipeline run twice under slightly different hardware configurations. The files are located at:
- `/home/user/outputs_run1.csv`
- `/home/user/outputs_run2.csv`

Both files contain tabular numerical data (100 samples, 50 features) with no headers.

Your task is to write a Python script at `/home/user/validate_pipeline.py` that performs dimensionality reduction and correlation analysis to validate the reproducibility of the inference outputs. 

The script must perform the following steps exactly:
1. Load both CSV files using `numpy`.
2. Use `sklearn.decomposition.PCA` to fit a Principal Component Analysis model on `outputs_run1.csv` and reduce it to 2 components. Use `random_state=42` when initializing PCA.
3. Transform `outputs_run2.csv` into the same 2-dimensional space using the PCA model fitted on `outputs_run1.csv`.
4. Calculate the covariance matrix of the reduced `outputs_run1` dataset (using `numpy.cov` with `rowvar=False`) and compute its trace (the sum of the diagonal elements).
5. Calculate the Pearson correlation coefficient between the first principal component (PC1) of the reduced `outputs_run1` and the first principal component (PC1) of the reduced `outputs_run2` (using `numpy.corrcoef`).
6. Write the results to a text file at `/home/user/report.txt` in the following exact format (rounded to 4 decimal places):

```text
Covariance Trace: [value]
PC1 Correlation: [value]
```

Run your script to generate the `/home/user/report.txt` file.