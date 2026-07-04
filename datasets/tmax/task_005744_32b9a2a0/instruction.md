You are a Data Scientist working on a mathematical data cleaning pipeline. You have a dataset of user-item interaction features, but some target values are missing due to sensor failures.

Your task is to write a C++ program from scratch that implements a reproducible K-Nearest Neighbors (KNN) imputation pipeline to estimate these missing values.

Dataset details:
- File location: `/home/user/dataset.txt`
- Format: Space-separated values.
- Columns: `ID X1 X2 Y`
- `ID` is an integer identifier.
- `X1` and `X2` are integer features.
- `Y` is a floating-point target value. If `Y` is missing, it is represented as `?`.

Pipeline Requirements:
1. **Model Architecture & Similarity Search**: Implement a KNN regressor. 
   - Use the **Manhattan distance** (L1 norm) between the `(X1, X2)` feature vectors to find the nearest neighbors.
   - **Tie-breaking**: If two points have the exact same distance to the query point, the point with the smaller `ID` must be considered "closer".
   - The predicted `Y` is the simple arithmetic mean of the `Y` values of the `K` nearest neighbors.

2. **Cross-Validation & Hyperparameter Tuning**: 
   - Isolate all rows that have a known `Y` value.
   - Perform Leave-One-Out Cross-Validation (LOOCV) on these complete rows to find the optimal `K` among the choices `K = 1, 2, 3`.
   - The optimal `K` is the one that minimizes the overall Mean Squared Error (MSE) across all LOOCV iterations. If there's a tie in MSE, pick the smaller `K`.

3. **Imputation & Reporting**:
   - Once the optimal `K` is found, use it to impute the missing `Y` values (the `?` entries). When imputing, use *all* complete rows as the reference set.
   - Create a file `/home/user/optimal_k.txt` containing only the integer value of the optimal `K`.
   - Create a file `/home/user/imputed.txt` containing the imputed values. Each line should contain `ID Imputed_Y`, space-separated. The `Imputed_Y` must be formatted to exactly 2 decimal places. Order the rows by `ID` in ascending order.

Constraints:
- You must write the solution in C++ (e.g., `/home/user/clean.cpp`). 
- You may only use the C++ standard library. Do not use external libraries like Eigen or Boost.
- Compile your program using `g++ -O3 /home/user/clean.cpp -o /home/user/clean` and run it.