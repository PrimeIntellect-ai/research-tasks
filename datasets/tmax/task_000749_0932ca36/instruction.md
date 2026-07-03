You are acting as a data analyst. I have a CSV file at `/home/user/sales.csv` containing housing data with two columns: `sqft` and `price`. The data is quite messy, and some rows contain strings, malformed numbers (like commas inside the numbers), or missing values.

Your task is to write a Go program that sets up the analysis environment, enforces a strict data schema, and performs a simple linear regression. 

Here are the requirements:
1. **Analysis Environment**: Initialize a Go module in `/home/user/analysis` and create your Go script (`main.go`) there. You may use standard library packages or third-party packages (like `gonum.org/v1/gonum/stat`) if you configure your module correctly.
2. **Data Schema Enforcement**: Read `/home/user/sales.csv`. Enforce a strict schema where both `sqft` and `price` must be parseable as standard 64-bit floats using Go's `strconv.ParseFloat` (after stripping leading/trailing whitespace). Do not attempt to clean out commas or currency symbols; simply *drop* any row that fails to parse directly as a float.
3. **Regression & Hypothesis Testing**: Using the valid rows, perform an Ordinary Least Squares (OLS) linear regression predicting `price` (Y) from `sqft` (X). Calculate:
   - The regression **slope**
   - The regression **intercept**
   - The **standard error of the slope** (used for hypothesis testing)
4. **Output**: Your Go program must output the results as a JSON file at `/home/user/regression_results.json` matching exactly this format:
   ```json
   {
     "valid_count": <integer_number_of_valid_rows>,
     "slope": <float>,
     "intercept": <float>,
     "slope_std_error": <float>
   }
   ```

Run your Go program so that the JSON file is created.