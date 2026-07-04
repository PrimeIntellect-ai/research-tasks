You are a data analyst who needs to process a local dataset by building a repeatable bash-driven pipeline.

A dataset is located at `/home/user/data.csv`. It contains 5 numeric columns: `x1`, `x2`, `x3`, `x4`, and `y`.

Write a Bash script at `/home/user/pipeline.sh` that automates the following end-to-end data processing workflow:
1. **Analysis Environment Setup:** The script should create a Python virtual environment at `/home/user/venv`.
2. **Package Installation:** Activate the virtual environment and install `pandas` and `scikit-learn` via `pip`.
3. **Data Processing:** The script should execute Python code (e.g., via a heredoc or by creating and running a `.py` file) that performs the following steps:
    a. Reads `/home/user/data.csv`.
    b. **Bootstrap Sampling:** Creates a bootstrap sample by sampling exactly 1000 rows with replacement from the dataset. Use random seed `42` for this sampling step.
    c. **Dimensionality Reduction:** Applies Principal Component Analysis (PCA) to the `x1`, `x2`, `x3`, and `x4` columns of the bootstrapped sample to reduce them to exactly 2 principal components. Use `random_state=42` for the PCA.
    d. **Bayesian Inference:** Fits a `BayesianRidge` regression model predicting the `y` column using the 2 PCA components as the input features. Use default parameters for the `BayesianRidge` model.
4. **Reporting:** The script must extract the estimated precision of the noise (the `alpha_` attribute of the fitted `BayesianRidge` model), round it to exactly 4 decimal places, and save this single numeric value to `/home/user/output.txt`.

Ensure your bash script is executable (`chmod +x /home/user/pipeline.sh`) and runs without user intervention. Do not hardcode the expected final answer.