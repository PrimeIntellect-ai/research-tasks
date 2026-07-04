You are an AI assistant acting as a Data Scientist. We have two datasets, `/home/user/data_a.csv` and `/home/user/data_b.csv`, which need to be merged, cleaned, and used to train a simple linear model. 

However, we want to strictly avoid "data leakage", a common pitfall where information from the test set influences the training phase (e.g., using the whole dataset for feature selection before splitting). 

Your task is to write a Go program (`/home/user/analyze.go`) that performs the following steps in this exact order:

1. **Initialize a Go module** in `/home/user/` named `ml_task`. You may install and use external libraries like `gonum.org/v1/gonum/stat` for mathematical functions.
2. **Data Joining:** Read both CSV files. They share a common `id` column. Perform an inner join on `id`.
3. **Data Cleaning:** Discard any merged row that contains the string `"NA"` or an empty value in any column.
4. **Sorting & Splitting:** 
   - Sort the cleaned dataset by `id` in ascending numerical order.
   - Split the dataset chronologically (by sorted index) into a `train` set and a `test` set. 
   - The `train` set must contain the first `80%` of the rows. Calculate this as `integer_division(total_clean_rows * 80, 100)`. The remaining rows form the `test` set.
5. **Feature Selection (Avoid Leakage):** 
   - Using **ONLY the `train` set**, calculate the Pearson correlation coefficient between each feature column (`f1`, `f2`, `f3`, `f4`) and the target column `y`.
   - Identify the feature with the highest absolute correlation to `y`.
6. **Model Training:** 
   - Using **ONLY the `train` set**, fit a simple linear regression model ($y = mx + c$) where the independent variable $x$ is the single best feature identified in step 5, and $y$ is the target.
7. **Model Evaluation:**
   - Predict `y` for the `test` set using the trained slope ($m$) and intercept ($c$).
   - Calculate the Mean Squared Error (MSE) of these predictions on the `test` set.
8. **Output:** 
   - Generate a JSON file at `/home/user/results.json` containing the selected feature, the slope, the intercept, and the test MSE. 

Format the JSON exactly with these keys and round the float values to 4 decimal places:
```json
{
  "selected_feature": "fX",
  "slope": 1.2345,
  "intercept": -0.1234,
  "test_mse": 5.6789
}
```

Do not create any files outside of `/home/user/`. Use standard Go formatting and conventions. Run the program to generate the `results.json` file.