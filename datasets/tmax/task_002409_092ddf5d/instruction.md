You are an ML engineer preparing a robust data pipeline for a new regression model. 

We have a custom Go package for tabular data processing called `tabular`, which handles joining multi-source data and missing value imputation. Its source code is vendored at `/app/vendor/tabular`. 

Recently, our pipeline started producing completely empty datasets (zero rows output) whenever missing values are encountered, similar to a rendering script producing blank plots due to a misconfiguration. The library is dropping all rows with nulls instead of imputing them. 

Your task is to:
1. Identify and fix the perturbation in the vendored `tabular` package located at `/app/vendor/tabular`. (Hint: Look for a hardcoded configuration or flag that forcibly disables imputation and drops rows).
2. Write a Go program at `/home/user/filter_data.go` that takes a single CSV file path as a command-line argument.
3. Your Go program must:
   - Use the fixed `github.com/data-prep/tabular` package (set up a `go.mod` with a `replace` directive pointing to `/app/vendor/tabular`).
   - Read the input CSV.
   - Join it with the reference metadata file located at `/app/data/metadata.csv` on the column `user_id`.
   - Apply a filter to drop any rows where the computed feature `risk_score` is an outlier (defined as `risk_score > 100.0` or `risk_score < 0.0`).
   - Print the sanitized CSV to standard output. 

You must ensure your program rejects invalid adversarial data while preserving clean data. We have provided test files in `/app/corpus/clean/` and `/app/corpus/evil/`. 
- Every file in the clean corpus has valid `risk_score` values (after imputation and join) and should result in rows being printed.
- Every file in the evil corpus is entirely composed of malicious outliers or un-joinable IDs, and must result in exactly 0 data rows printed (header only or empty output).

Create the fully working `/home/user/filter_data.go` and fix the vendored package.