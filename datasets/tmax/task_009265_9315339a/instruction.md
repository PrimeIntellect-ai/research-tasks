You are a data analyst tasked with building a robust data processing and modeling pipeline. You have been provided with a raw dataset that contains several data quality issues and mixed formats. 

Your goal is to write a Python script `/home/user/pipeline.py` that processes the dataset, engineers features, enforces the correct schema, trains a Ridge regression model, and generates predictions.

**Dataset Location:**
`/home/user/data/raw_data.csv`

**Columns in the dataset:**
- `id`: Unique identifier (integer)
- `date`: Date of the transaction, but unfortunately it contains mixed formats (e.g., `YYYY-MM-DD` and `MM/DD/YYYY`).
- `zip_code`: Store location zip code (currently numeric, but must be treated as categorical).
- `price`: The price of the item, currently formatted as a string with currency symbols and commas (e.g., `$1,234.56`).
- `marketing_spend`: Continuous numerical feature (float).
- `sales`: The target variable to predict (float).

**Pipeline Requirements:**
1. **Schema Enforcement & Data Cleaning**:
   - Parse the `date` column into datetime objects (handling the mixed formats) and create a new integer column `month` (1-12).
   - Clean the `price` column by removing the `$` and `,` characters, and convert it to a float.
   - Convert the `zip_code` column to strings so it is treated as a categorical variable.
2. **Feature Engineering**:
   - One-hot encode the `zip_code` column using `pandas.get_dummies()`. Do not drop the first category. Use the prefix `zip_code` so the resulting columns are exactly: `zip_code_10001`, `zip_code_20002`, `zip_code_30003`, `zip_code_40004`.
3. **Modeling**:
   - Define your feature matrix `X` to include exactly the following columns in this specific order: 
     `['month', 'price', 'marketing_spend', 'zip_code_10001', 'zip_code_20002', 'zip_code_30003', 'zip_code_40004']`
   - Define your target variable `y` as the `sales` column.
   - Initialize and train a Ridge regression model using `sklearn.linear_model.Ridge(alpha=1.0, random_state=42)` on the entire dataset.
4. **Prediction and Evaluation**:
   - Generate predictions for the same dataset.
   - Save the predictions to `/home/user/predictions.csv`. The file must contain exactly two columns: `id` and `predicted_sales`.
   - Calculate the Mean Squared Error (MSE) of your predictions.
   - Save the MSE to a file `/home/user/metrics.txt` in the exact format: `MSE: <value>` where `<value>` is rounded to 2 decimal places (e.g., `MSE: 38210.45`).

Write the script, execute it, and ensure that both `/home/user/predictions.csv` and `/home/user/metrics.txt` are generated successfully with the correct values.