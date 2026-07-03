You are assisting a data researcher in building a reproducible ETL and modeling pipeline. The researcher is struggling with a common pandas pitfall where missing values silently convert integer columns to floats, which breaks their downstream string-hashing and grouping logic. 

Your task is to write a complete Python pipeline script `/home/user/pipeline.py` that reads data, performs ETL, trains a model, and predicts on test data.

**Data Provided:**
You have two files:
- `/home/user/train.csv`: Columns `id`, `category_id`, `v1`, `v2`, `target`
- `/home/user/test.csv`: Columns `id`, `category_id`, `v1`, `v2`

Notice that `category_id` contains empty values (missing data). 

**Pipeline Requirements:**
1. **Dependency Management:** Install `pandas` and `scikit-learn` if they are not already present.
2. **Missing Value Handling:** Replace any missing values in `category_id` with `-1`. 
3. **The Float Trap:** You must ensure that `category_id` is treated strictly as an integer, not a float (e.g., `10`, not `10.0`). 
4. **Feature Engineering 1 (String Hashing):** Create a new column `hash_key` formatted exactly as `"{category_id}_{id}"`. If you fail to prevent the float conversion, this will incorrectly become something like `10.0_1`, which is strictly forbidden and will fail validation.
5. **Feature Engineering 2 (Target/Group Encoding):** Create a new column `cat_mean_v1`. This is the mean of `v1` for each `category_id`. 
   - *Crucial:* You must compute these group means ONLY on the training data. 
   - Map these computed means onto both the training and test sets. 
   - If a `category_id` appears in the test set but wasn't in the training set, its `cat_mean_v1` should be filled with `0.0`.
6. **Modeling:** Train a Logistic Regression model using `sklearn.linear_model.LogisticRegression`. 
   - Use features: `v1`, `v2`, and `cat_mean_v1`.
   - Initialize the model with exactly `random_state=42` and `solver='lbfgs'`. Leave other parameters as default.
   - Train on the processed training set (where target is the `target` column).
7. **Prediction & Output:** Predict the targets for the processed test set. Save the results to `/home/user/predictions.csv`.

**Output Format:**
`/home/user/predictions.csv` must be a CSV file with exactly a header and three columns in this order:
`id,hash_key,prediction`

You may use standard terminal tools to install dependencies and run your script. Make sure your script runs autonomously when executed via `python3 /home/user/pipeline.py`.