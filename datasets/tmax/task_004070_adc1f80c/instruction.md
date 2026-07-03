You are a Data Engineer building an automated ETL and modeling pipeline for high-frequency sensor data. 

Your task is to write a C++ program that processes a dataset, handles missing values and outliers, and performs hyperparameter tuning for a Ridge Regression model using Cross-Validation. 

You must write a C++ program at `/home/user/etl_pipeline.cpp` that performs the following steps in order:

1. **Load Data**: Read `/home/user/sensor_data.csv`. The CSV has headers: `timestamp,sensor1,sensor2,target`. 
   - Some values in `sensor2` are `NaN`.
2. **Outlier Removal**: 
   - Compute the mean and population standard deviation of `sensor1` across all rows.
   - Remove any rows where the absolute Z-score of `sensor1` is strictly greater than 3.0. 
   - Keep track of the number of rows removed.
3. **Missing Value Imputation**: 
   - After outlier removal, compute the mean of the valid (non-NaN) values in `sensor2`.
   - Replace all `NaN` values in `sensor2` with this mean.
4. **Model Training & Cross-Validation**:
   - We want to predict `target` using `sensor1` and `sensor2`.
   - Construct a feature matrix $X$ where each row is `[1.0, sensor1, sensor2]` (including an intercept term). Let $y$ be the `target` vector.
   - Implement Ridge Regression analytically: $w = (X^T X + \alpha I)^{-1} X^T y$, where $I$ is the identity matrix of the same dimension as $X^T X$.
   - Implement 5-fold cross-validation to find the best penalty parameter $\alpha$ from the set: `{0.1, 1.0, 10.0}`.
   - **Splitting rule**: Divide the cleaned dataset into 5 contiguous, equal-sized folds. (Assume the number of rows after outlier removal is perfectly divisible by 5). Fold 1 is the first $N/5$ rows, Fold 2 is the next $N/5$, etc. 
   - For each $\alpha$, compute the Mean Squared Error (MSE) on the validation fold for all 5 splits, and calculate the average validation MSE.
5. **Output**: Write the results to `/home/user/pipeline_results.json` with the exact following format:
```json
{
  "outliers_removed": 0,
  "imputed_mean": 0.0000,
  "best_alpha": 0.0,
  "cv_mse_best_alpha": 0.0000
}
```
*Note: Format floating-point numbers to 4 decimal places.*

**Environment & Constraints:**
- You are working in a standard Linux environment.
- You should install the `Eigen3` library (`sudo apt-get update && sudo apt-get install -y libeigen-dev`) to handle matrix operations.
- Compile your C++ program using `g++` (e.g., `g++ -O3 -I /usr/include/eigen3 etl_pipeline.cpp -o etl_pipeline`) and execute it.