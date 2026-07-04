You are a data engineer building a reproducible ETL pipeline. Your current task is to implement a dimensionality reduction and feature selection step in Go to remove highly correlated features before passing the data to a downstream model.

Setup:
1. A dataset is located at `/home/user/data.csv`. It contains 5 columns: `F1`, `F2`, `F3`, `F4`, and `Target`. All values are numeric.
2. Create a new Go module in the directory `/home/user/pipeline` named `etl`.
3. Write a Go program `/home/user/pipeline/etl.go` that reads `/home/user/data.csv`.

Pipeline Requirements:
1. Compute the Pearson correlation coefficient between all pairs of the feature columns (`F1`, `F2`, `F3`, `F4`). Do not include `Target` in the correlation calculations.
2. Identify any pairs of features that have an absolute correlation greater than or equal to `0.90`.
3. For any highly correlated pair, drop the feature that appears later in the column order (e.g., if `F1` and `F3` are correlated >= 0.90, drop `F3`).
4. Write the retained features and the `Target` column to a new file at `/home/user/pipeline/cleaned.csv`.
5. The output CSV must include the header row, maintain the original row order, use comma separation, and format all floating-point numbers to exactly 1 decimal place (e.g., `1.0`, `2.5`). The `Target` column should also be formatted to 1 decimal place.

Execute your Go program so that `/home/user/pipeline/cleaned.csv` is successfully generated. You may use standard Go libraries or third-party packages (like `gonum.org/v1/gonum/stat`) if you initialize and fetch them properly.