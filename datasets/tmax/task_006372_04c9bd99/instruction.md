You are a data systems engineer tasked with building a robust ETL and modeling pipeline in Go. We have a raw dataset from our manufacturing sensors, but the data extraction process introduced a subtle flaw: one of the integer columns contains `"NaN"` strings for missing values.

Your objective is to write a Go program that cleans this data, performs linear algebra operations to train a regression model, and calculates statistical confidence intervals on the predictions.

**Task Steps:**
1. Initialize a Go module in `/home/user/pipeline`. You may use external packages like `gonum.org/v1/gonum` for linear algebra and statistics.
2. Read the raw dataset located at `/home/user/data/sensors.csv`.
3. **ETL & Imputation:** 
   - The `vibration` column represents integer counts, but missing values are recorded as `"NaN"`.
   - Calculate the mean of all valid (non-NaN) `vibration` values.
   - Impute the missing `"NaN"` values with this mean, **rounded to the nearest integer** (half away from zero).
4. **Model Training:**
   - Construct a feature matrix $X$ using the columns in this exact order: `bias` (a constant 1.0 for all rows), `vibration`, `temperature`, and `pressure`.
   - The target vector $y$ is the `risk` column.
   - Use Ordinary Least Squares (OLS) to solve for the linear regression weights: $w = (X^T X)^{-1} X^T y$.
5. **Evaluation & Hypothesis Testing:**
   - Compute the predicted risk $\hat{y}$ for all rows using your trained weights.
   - Calculate the 95% confidence interval for the **mean** of the predicted risk values $\hat{y}$. 
   - Use the standard error of the mean formula ($SE = \frac{s}{\sqrt{n}}$) and a Z-score of exactly `1.96` for the 95% CI. ($s$ is the sample standard deviation of $\hat{y}$).
6. **Output:**
   - Write the results to a JSON file at `/home/user/results.json` matching this exact structure:
   ```json
   {
     "weights": [w_bias, w_vibration, w_temperature, w_pressure],
     "mean_prediction": 1.2345,
     "ci_lower": 1.1000,
     "ci_upper": 1.3680
   }
   ```

**Constraints:**
- Your Go code must compile and run successfully.
- Do not use Python or other languages to solve the core task, though shell utilities are permitted for setup.
- Output JSON floats should not be strictly rounded in the file, but standard 64-bit float precision is expected.