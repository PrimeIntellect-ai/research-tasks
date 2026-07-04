You are a data scientist tasked with cleaning a messy dataset and extracting statistical insights using a multi-language workflow.

You have been provided with a dataset at `/home/user/sensor_data.csv` containing four columns: `timestamp`, `sensor_A`, `sensor_B`, and `target`.

Your objective is to perform data cleaning in Python and statistical modeling/bootstrapping in R.

**Phase 1: Data Cleaning (Python)**
Write a Python script to process `/home/user/sensor_data.csv` according to these rules:
1. **Missing Values:** The `sensor_A` column contains missing values (`NaN`). Fill these missing values using standard linear interpolation based on the index/row order.
2. **Outliers:** The `sensor_B` column contains extreme outliers. Calculate the mean and standard deviation of `sensor_B` (including the outliers). Remove any rows where the `sensor_B` value is strictly greater than 3 standard deviations away from the mean or strictly less than 3 standard deviations away from the mean.
3. Save the cleaned dataset to `/home/user/cleaned_data.csv`.

**Phase 2: Statistical Modeling & Bootstrapping (R)**
Write an R script to analyze `/home/user/cleaned_data.csv`:
1. **Bootstrapping:** Calculate the 95% confidence interval for the mean of the `target` column using the percentile bootstrap method. 
   - You MUST use exactly `1000` bootstrap resamples.
   - You MUST set the random seed to `42` (`set.seed(42)`) immediately before running the bootstrap loop/sampling.
   - Calculate the 2.5th and 97.5th percentiles of the bootstrapped means using R's default `quantile()` function.
2. **Modeling:** Train a standard Ordinary Least Squares (OLS) linear regression model predicting `target` using `sensor_A` and `sensor_B` as predictors (i.e., `target ~ sensor_A + sensor_B`). Extract the Multiple R-squared value of this model.

**Phase 3: Reporting**
Output your final results into a JSON file located at `/home/user/results.json` with exactly the following keys:
- `"clean_row_count"`: (integer) The number of rows in `cleaned_data.csv`.
- `"bootstrap_lower"`: (float) The 2.5th percentile of the bootstrapped means, rounded to 2 decimal places.
- `"bootstrap_upper"`: (float) The 97.5th percentile of the bootstrapped means, rounded to 2 decimal places.
- `"r_squared"`: (float) The Multiple R-squared of the linear model, rounded to 4 decimal places.

Ensure all scripts are run and the final `results.json` is generated successfully.