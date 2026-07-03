You are a data scientist tasked with cleaning a dataset, performing correlation analysis, logging your experiment metrics, and serving the cleaned data via a local API framework.

We use a proprietary local API framework called `miniserve` to share datasets with internal tools. The source code for this framework is vendored at `/app/miniserve-0.1.0/`. However, it currently has a bug where it crashes with a `NameError` when trying to return JSON responses. 

Your tasks are:

1. **Fix the Framework:**
   Investigate and fix the bug in `/app/miniserve-0.1.0/miniserve/response.py` so that it can successfully return JSON responses. After fixing it, install it locally in your environment (e.g., `pip install -e /app/miniserve-0.1.0/`).

2. **Data Cleaning & Joining:**
   You have two datasets:
   - `/home/user/data/transactions.csv` (columns: `user_id`, `transaction_date`, `amount`)
   - `/home/user/data/users.csv` (columns: `user_id`, `age`, `signup_date`)
   
   Perform the following transformations:
   - Join the transactions and users on `user_id` (inner join).
   - Drop any rows where `age` is missing (NaN/null).
   - For missing values in the `amount` column, impute them using the global mean of the `amount` column (calculated *after* dropping missing ages).
   - Save the cleaned, joined dataset to `/home/user/data/cleaned_dataset.csv`.

3. **Experiment Tracking & Correlation:**
   - Calculate the Pearson correlation coefficient between `age` and `amount` on the fully cleaned dataset.
   - Save your metrics to an experiment tracking log at `/home/user/experiment_log.json`. The file must be valid JSON with exactly two keys:
     - `"mean_amount"`: The mean amount calculated and used for imputation (as a float).
     - `"correlation_age_amount"`: The Pearson correlation calculated (as a float).

4. **Data Serving:**
   Write a script `/home/user/serve_data.py` using the fixed `miniserve` package to serve your results. Your server must:
   - Listen on `0.0.0.0` port `8888`.
   - Implement `GET /api/stats` which returns the contents of `/home/user/experiment_log.json`.
   - Implement `GET /api/data` which returns the first 10 rows of the cleaned dataset as a JSON list of dictionaries.
   - Require an authorization header for all requests: `Authorization: Bearer ds-secret`. Return an HTTP 401 if this is missing or incorrect.

Start the server in the background and leave it running.