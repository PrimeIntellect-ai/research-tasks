You are tasked with fixing a broken data processing pipeline and implementing a specific ETL and regression script. 

First, there is a third-party package vendored at `/app/data_purify` that our team uses to clean tabular data. Recently, someone modified the package and accidentally broke the filtering logic. Currently, it acts like a misconfigured backend and "blanks out" the entire dataset by returning empty lists. 
1. Inspect the source code of `data_purify` in `/app/data_purify` and fix the bug in the `filter_valid` function so it correctly removes records where the `category` key equals `"unknown"`, but keeps all other valid records.
2. Install the fixed package in your environment (e.g., using pip).

Next, write a Python script at `/home/user/process.py` that acts as a robust data processing pipeline:
1. It must read a JSON-encoded list of dictionaries from **standard input**. Each dictionary will have the keys `"x"` (float), `"y"` (float), and `"category"` (string).
2. It must use the fixed `data_purify.cleaner.filter_valid` function to filter the dataset.
3. Using the cleaned dataset, compute the exact Pearson correlation coefficient between `x` and `y`.
4. If the correlation is strictly greater than `0.5`, perform a Simple Linear Regression (Ordinary Least Squares) to predict `y` from `x`. Calculate the predicted value of `y` when `x = 100.0`. 
5. If the correlation is less than or equal to `0.5`, or if the correlation is undefined (e.g., due to zero variance or less than 2 valid records), the predicted value should default to `0.0000`.
6. Print ONLY the predicted value of `y` to **standard output**, formatted to exactly 4 decimal places (e.g., `42.1234`).

You must use the population formulas for Covariance and Variance (divide by N, not N-1) if calculating manually, or the equivalent library defaults, to ensure deterministic exact behavior. For example:
- $mean(x) = \sum x / N$
- $Cov(x,y) = \sum (x_i - mean(x))(y_i - mean(y)) / N$
- $Var(x) = \sum (x_i - mean(x))^2 / N$
- $Pearson = Cov(x,y) / \sqrt{Var(x) * Var(y)}$
- $m = Cov(x,y) / Var(x)$
- $c = mean(y) - m * mean(x)$
- $Prediction = m * 100.0 + c$

Make sure your script handles standard input correctly and outputs exactly one line with the formatted number.