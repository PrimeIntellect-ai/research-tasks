You are a Machine Learning Engineer tasked with preparing a training dataset and extracting preliminary statistical insights. You need to write a Go program to process a raw text dataset, perform custom tokenization, and calculate specific statistical metrics (correlation and covariance) to evaluate feature viability.

Your workspace is `/home/user`. A dataset has been provided at `/home/user/data.csv` with the following columns: `id`, `text`, `engagement_score`.

Write a Go program located at `/home/user/ml_prep/analyzer.go` (you will need to initialize a Go module in that directory) that performs the following steps:

1. **Tokenization and Dataset Preparation**:
   - Read the `/home/user/data.csv` file.
   - For each row, tokenize the `text` column: 
     - Convert the entire string to lowercase.
     - Replace all non-alphanumeric characters (anything that is not a letter `a-z` or number `0-9`) with a single space `" "`.
     - Split the string by spaces.
     - Discard any empty tokens.
   - Count the number of resulting tokens for each row (this is the `token_count`).
   - Determine the presence of the exact token `"ai"` (boolean, `1` if present at least once, `0` if not).

2. **Correlation Analysis**:
   - Calculate the **Sample Pearson Correlation Coefficient** between the `token_count` (X) and the `engagement_score` (Y) across the *entire* dataset.

3. **Data Filtering & Covariance Analysis**:
   - Filter the dataset to keep **only** the rows where `token_count > 5`.
   - On this *filtered* dataset, calculate the **Sample Covariance** between the presence of the `"ai"` token (X, where 1=present, 0=absent) and the `engagement_score` (Y).

4. **Reporting**:
   - Your Go program should compute these values and output a JSON file at `/home/user/stats.json` with exactly the following structure (values should be floats, use at least 4 decimal places of precision internally, standard JSON marshalling is fine):
   ```json
   {
     "correlation_length_score": 0.123456,
     "covariance_ai_score": 0.056789,
     "filtered_count": 42
   }
   ```

**Constraints & Rules**:
- You must use Go (`go run analyzer.go` should execute successfully).
- You may use standard library packages or popular third-party statistical packages (like `gonum.org/v1/gonum/stat`) by running `go get`.
- The sample covariance and sample correlation formulas should use `N-1` in the denominator.
- Ensure the `stats.json` file is generated exactly at `/home/user/stats.json`.