You are a data scientist tasked with cleaning a messy dataset, engineering features, and building a strictly reproducible hyperparameter tuning pipeline. Your goal is to ensure that the pipeline yields the exact same results every time it is run, avoiding common sources of non-determinism in numerical libraries and machine learning algorithms.

We have a dataset located at `/home/user/housing_messy.csv`.

Please complete the following steps:

1. **Write a Python script at `/home/user/clean_and_tune.py`** that does the following:
   - Load `/home/user/housing_messy.csv` using pandas.
   - **Feature Engineering & Cleaning:** 
     - Fill any missing values in the `age` column with the median of the `age` column (computed before filling).
     - Create a new feature called `rooms_per_age` which is exactly `rooms / age`.
     - Define your feature matrix `X` using only these columns in this exact order: `rooms`, `age`, `rooms_per_age`, `income`.
     - Define your target vector `y` using the `price` column.
   - **Hyperparameter Tuning & Cross-Validation:**
     - Create a scikit-learn `Pipeline` with two steps: a `StandardScaler` and a `RandomForestRegressor`.
     - Configure the `RandomForestRegressor` to use a fixed `random_state=42` for reproducibility.
     - Set up a `KFold` cross-validator with `n_splits=5`, `shuffle=True`, and `random_state=42`.
     - Use `GridSearchCV` to tune the `max_depth` of the random forest over the values `[3, 5, 7]`. Set `n_estimators=50` (fixed). Use the `KFold` object for the `cv` parameter.
     - Fit the `GridSearchCV` on `X` and `y`.
   - **Reporting:**
     - The script must write the best `max_depth` parameter and the best mean cross-validated score (from `grid_search.best_score_`) to a file named `/home/user/reproducibility_log.txt`.
     - The format of `/home/user/reproducibility_log.txt` must be exactly two lines:
       ```
       Best max_depth: <integer>
       Best CV score: <float rounded to 4 decimal places>
       ```

2. **Write a bash script at `/home/user/run_pipeline.sh`** to execute your Python pipeline reproducibly:
   - The script must configure numerical library environment variables to enforce deterministic behavior. Specifically, export `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, and `PYTHONHASHSEED=42`.
   - The script must then execute your `/home/user/clean_and_tune.py` script.
   - Ensure the bash script is executable (`chmod +x`).

The automated testing framework will run `/home/user/run_pipeline.sh` multiple times to verify that the output in `/home/user/reproducibility_log.txt` remains strictly identical and matches the mathematically expected values.