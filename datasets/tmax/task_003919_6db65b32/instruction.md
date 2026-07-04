You are an ML Engineer preparing data and running a baseline evaluation using Go. Your team typically uses Python, but due to a performance mandate, you must implement this specific pipeline in Go. 

You have a raw dataset at `/home/user/raw_data.csv` with columns `ID,X1,X2,Y`. There is a known issue where missing values in integer columns often cause systems to silently convert the entire column to floats (similar to Pandas' default behavior). Your Go pipeline must strictly prevent this.

Write a Go program at `/home/user/pipeline.go` that performs the following:

1. **ETL & Imputation**: 
   - Read `/home/user/raw_data.csv`.
   - For the `X1` column, some values are missing (represented by an empty string). Impute these missing values with the **integer median** of all valid `X1` values (if the median falls between two integers, round down to the nearest integer). 
   - Ensure `X1` is strictly treated and written as an integer.

2. **Feature Engineering**:
   - Create a new feature `X3` which is the product of `X1` and `X2` (`X3 = X1 * X2`).

3. **Hyperparameter Tuning via Cross-Validation**:
   - You are testing a simple threshold model to predict `Y`. The model predicts $\hat{Y} = 100$ if $X3 \ge T$, otherwise $\hat{Y} = 0$.
   - Perform 5-fold cross-validation to find the optimal threshold $T$ from the candidate set $\{10, 20, 30, 40, 50\}$.
   - The folds must be sequential without shuffling (Fold 1: rows 0-19%, Fold 2: 20-39%, etc.). Assume the total number of rows is perfectly divisible by 5.
   - For each $T$, calculate the Mean Squared Error (MSE) between the predictions $\hat{Y}$ and actual `Y` for the validation set in each fold. Average the MSE across all 5 folds.

4. **Output Requirements**:
   - Save the cleaned, engineered dataset to `/home/user/clean_data.csv` with headers `ID,X1,X2,X3,Y`.
   - Save the evaluation results to `/home/user/result.txt` in exactly this format:
     ```
     Optimal T: <optimal_T>
     Best MSE: <mse_value_formatted_to_2_decimal_places>
     ```

To complete the task, write the Go code, compile it, and run it so that `clean_data.csv` and `result.txt` are generated.