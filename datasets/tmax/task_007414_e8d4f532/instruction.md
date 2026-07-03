You are an AI assistant helping a researcher organize and analyze a dataset from a recent set of experiments. The dataset is located at `/home/user/experiment_data.csv`.

Your task involves three steps: package management, Bayesian inference, and regression modeling.

1. **Environment Setup**: Ensure that `pandas` and `scikit-learn` are installed in the Python environment.
2. **Bayesian Inference**: The researcher wants to estimate the success rate of experiments specifically in "Group A". 
   - Filter the dataset for rows where the `group` column is exactly `'A'`.
   - The data contains `trials` (total attempts) and `successes` (successful attempts) for each experiment. 
   - Assume a Beta-Binomial conjugate model with a uniform prior (Alpha = 1, Beta = 1).
   - Calculate the posterior Alpha and Beta parameters by aggregating all trials and successes for Group A.
   - Save the posterior parameters as comma-separated integers (Alpha,Beta) to a file named `/home/user/posterior_params.txt`.
3. **Classification Modeling**: The researcher also wants to classify the `outcome_class` (0 or 1) based on the environmental conditions.
   - Using the *entire dataset* (both Group A and B), train a standard Logistic Regression model using `sklearn.linear_model.LogisticRegression`.
   - Use `temperature` and `pressure` as the features (in that order), and `outcome_class` as the target.
   - Initialize the model with `random_state=42` and `penalty=None` (no regularization) to ensure reproducible results. Fit it on the entire dataset.
   - Extract the model's intercept and coefficients.
   - Save these values comma-separated (Intercept, Temperature_Coefficient, Pressure_Coefficient) rounded to exactly 4 decimal places to `/home/user/regression_coefs.txt`.

Write and execute the necessary scripts to produce these two output files.