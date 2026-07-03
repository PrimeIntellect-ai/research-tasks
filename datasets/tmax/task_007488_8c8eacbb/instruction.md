You are an MLOps engineer responsible for building a robust data processing and artifact tracking pipeline. We have a raw experiment dataset located at `/home/user/raw_experiment.csv` that contains sensor readings and a target metric.

Your task is to build a reproducible pipeline in Go that cleans this data, performs a linear regression using matrix operations, applies bootstrap sampling to estimate confidence intervals, and outputs tracked artifacts.

Here are the precise requirements:

1. **Pipeline Initialization**:
   - Create a Go module named `mlops-pipeline` in `/home/user/pipeline`.
   - Write your Go code in `/home/user/pipeline/main.go`.
   - You may use `gonum.org/v1/gonum/mat` and `gonum.org/v1/gonum/stat` for linear algebra and statistics.

2. **Data Cleaning (Missing Values & Outliers)**:
   - Read `/home/user/raw_experiment.csv`. The file has a header: `ID,X1,X2,Y`.
   - **Step A:** Remove any rows that contain empty/missing values in any column.
   - **Step B:** Calculate the mean and standard deviation of the `Y` column for the remaining rows. Remove any rows where the `Y` value has a Z-score strictly greater than `2.0` (i.e., $|Y - \mu_Y| / \sigma_Y > 2.0$). 
   - Save this cleaned dataset to `/home/user/artifacts/cleaned_data.csv` (include the header).

3. **Linear Algebra & Regression**:
   - Fit a Multiple Linear Regression model: $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2$.
   - Construct the design matrix $X$ (with a column of 1s for the intercept $\beta_0$, followed by $X_1$ and $X_2$) and the response vector $Y$ using the cleaned data.
   - Calculate the coefficients using the Ordinary Least Squares (OLS) closed-form solution: $\beta = (X^T X)^{-1} X^T Y$. Use `gonum/mat` to perform these matrix operations.

4. **Bootstrap Sampling**:
   - We need to track the stability of the $\beta_1$ coefficient.
   - Perform 1000 bootstrap iterations. In each iteration:
     - Sample $N$ rows *with replacement* from the cleaned dataset (where $N$ is the number of rows in the cleaned dataset).
     - Calculate the OLS coefficients for this bootstrap sample.
     - Record the $\beta_1$ coefficient.
   - Calculate the 95% confidence interval for $\beta_1$ using the percentile method (find the 2.5th percentile and 97.5th percentile of the 1000 bootstrap estimates). 
   - *Crucial for reproducibility*: Use `math/rand` and initialize your random number generator exactly once before the bootstrap loop using `rng := rand.New(rand.NewSource(42))`. Use `rng.Intn(N)` to select row indices. Sort the bootstrap estimates in ascending order to find the percentiles (index `0.025 * 1000 = 25` for lower, `0.975 * 1000 = 975` for upper).

5. **Artifact Generation**:
   - Create a directory `/home/user/artifacts` if it doesn't exist.
   - Output a JSON file at `/home/user/artifacts/metrics.json` with the following structure (round floats to 4 decimal places):
     ```json
     {
       "cleaned_row_count": 85,
       "beta1_estimate": 3.4567,
       "beta1_ci_lower": 3.1234,
       "beta1_ci_upper": 3.8901
     }
     ```
     *(The numbers above are just examples).*

6. **Execution**:
   - Write a shell script at `/home/user/run_pipeline.sh` that initializes the Go module (if not already done), downloads dependencies, builds the Go executable, and runs it to produce the artifacts.