You are an AI assistant helping a data science researcher organize and analyze a set of numerical datasets whose metadata has been lost. 

The datasets are located in `/home/user/datasets/` and are named `dataset_A.csv`, `dataset_B.csv`, and `dataset_C.csv`. 

Your task is to analyze these datasets, perform specific mathematical and statistical modeling tasks, and output the exact results to specified files. You may use any language (Python, R, bash tools, etc.) to perform the analysis.

**Task Requirements:**

1. **Dataset A Analysis (Exact OLS Regression):**
   - `dataset_A.csv` contains features `x1`, `x2`, and a target variable `y`.
   - Calculate the exact Ordinary Least Squares (OLS) coefficients for a multiple linear regression model predicting `y` from `x1` and `x2`, including an intercept.
   - Save the coefficients (Intercept, x1 coefficient, x2 coefficient) as a comma-separated list of numbers rounded to 2 decimal places to `/home/user/ols_coeffs.txt`. Example format: `1.23,4.56,-7.89`

2. **Dataset B Analysis (Information Theory):**
   - `dataset_B.csv` contains a binary classification target column named `label`.
   - Calculate the Shannon Entropy (in bits, i.e., base 2) of the `label` distribution.
   - Save the entropy value rounded exactly to 4 decimal places to `/home/user/entropy.txt`. Example format: `0.1234`

3. **Dataset C Analysis (Model Inference & Evaluation):**
   - `dataset_C.csv` contains features `f1`, `f2`, and a ground-truth column `target`.
   - You need to evaluate a specific pre-determined model architecture on this dataset. 
   - The model is a linear regression with the following weights: `Intercept = 0.5`, `weight_f1 = 1.5`, `weight_f2 = -1.0`.
   - Apply this model to the features in `dataset_C.csv` to generate predictions.
   - Calculate the Root Mean Squared Error (RMSE) between the predictions and the actual `target` values.
   - Save the RMSE rounded exactly to 4 decimal places to `/home/user/rmse.txt`.

Ensure your calculations are highly accurate and that the final output files strictly adhere to the requested formats. You will need to write and execute scripts in the terminal to accomplish this.