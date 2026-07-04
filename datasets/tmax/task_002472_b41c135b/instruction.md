You are a data scientist working on a C++ data processing pipeline. We recently noticed our pipeline silently corrupts integer features when it encounters missing values, implicitly casting them to 0 or NaN and skewing downstream statistical models.

Your task is to build a robust C++ pipeline that reads a dataset, correctly handles missing integer data, performs a hypothesis test, and trains a baseline model.

**Environment Setup:**
1. You will need to install any necessary tools and C++ libraries to perform matrix operations and write JSON. We recommend installing `g++`, `libarmadillo-dev` (for math/statistics), and `nlohmann-json3-dev` (for JSON output). 
2. Ensure your build compiles with `-std=c++17` and links against `armadillo`.

**Data Description:**
You have a dataset at `/home/user/dataset.csv` with a header row and three columns:
- `group`: An integer (0 or 1)
- `feature_x`: An integer, but some values are missing (represented by an empty string `""`).
- `target_y`: A floating-point number.

**Pipeline Requirements:**
Write a C++ program at `/home/user/pipeline.cpp` that performs the following steps sequentially:

1. **Data Cleaning (Imputation):**
   - Read `/home/user/dataset.csv`.
   - Identify all valid (non-missing) integers in `feature_x`.
   - Calculate the **median** of these valid integers. If there is an even number of valid integers, take the arithmetic mean of the two middle values and use the `std::floor` of that mean.
   - Replace all missing values in `feature_x` with this computed median integer.

2. **Hypothesis Testing:**
   - Conduct a standard two-sample independent Student's t-test (assuming equal variances) on `target_y` between `group = 0` and `group = 1`.
   - Calculate the t-statistic.

3. **Model Training:**
   - Using the cleaned `feature_x` as the independent variable and `target_y` as the dependent variable, train a Simple Linear Regression model (Ordinary Least Squares) on the entire dataset.
   - Calculate the regression slope (weight) and intercept (bias).

4. **Output Generation:**
   - Write the results to `/home/user/results.json` in exactly this format:
     ```json
     {
       "imputed_feature_x_median": 42,
       "t_statistic": 1.2345,
       "regression_slope": 0.5678,
       "regression_intercept": 10.1234
     }
     ```
   - Float values should be rounded to 4 decimal places.

Compile your code, run the pipeline, and ensure `/home/user/results.json` is generated correctly.