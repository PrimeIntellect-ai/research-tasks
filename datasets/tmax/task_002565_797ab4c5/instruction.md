You are a data scientist cleaning a dataset for model evaluation. You have two files representing model predictions and ground-truth values. You need to write a Go script to join the datasets, validate the predictions, calculate the absolute error, and format the output.

Here are the details:
- **Predictions file**: `/home/user/predictions.csv` (columns: `id`, `predicted_value`)
- **Ground-truth file**: `/home/user/truth.csv` (columns: `id`, `actual_value`, `category`)

Write a Go program at `/home/user/validate.go` that does the following:
1. Reads both CSV files.
2. Joins the records on the `id` field.
3. Validates the `predicted_value`. A prediction is considered **valid** only if it is between `0.0` and `100.0` (inclusive). Discard any rows with invalid predictions.
4. For valid predictions, calculate the Absolute Error: `|predicted_value - actual_value|`.
5. Write the results to a new CSV file at `/home/user/cleaned_metrics.csv` with the exact header: `id,category,abs_error`.
6. Format the `abs_error` to exactly 2 decimal places (e.g., `1.80`, `0.50`).

Once the code is written, run the Go script so that `/home/user/cleaned_metrics.csv` is produced. Do not use any third-party Go packages (only the standard library like `encoding/csv`, `os`, `strconv`, `math`, `fmt`).