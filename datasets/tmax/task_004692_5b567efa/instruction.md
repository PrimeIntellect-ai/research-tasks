You are taking over a machine learning project from a junior engineer. They have built an ETL and modeling script in Python, but their evaluation metrics are overly optimistic due to a classic data leakage bug: they are applying their data transformations (`fit_transform`) to the *entire* dataset before splitting it into training and testing sets.

Your task is to:
1. Review the existing script at `/home/user/train_pipeline.py`.
2. Refactor the code to eliminate the data leakage. You must ensure that the `SimpleImputer` and `StandardScaler` are **fitted only on the training data**, and then used to **transform** both the training and testing data.
3. You can either use `sklearn.pipeline.Pipeline` or manually apply `fit` and `transform` correctly. 
4. **Constraints:** 
   - You must retain the exact same preprocessing steps (`SimpleImputer(strategy='mean')` and `StandardScaler()`).
   - You must retain the exact same model (`LogisticRegression(random_state=42)`).
   - You must retain the exact same splitting strategy (`test_size=0.2, random_state=42`).
   - Keep the existing features and target column intact.
5. Install any necessary Python libraries in the user environment (e.g., `pandas`, `scikit-learn`).
6. Run the updated script.

The script currently outputs a file at `/home/user/metrics.json` containing the test set accuracy and the mean of the first feature (index 0) of the transformed test set. By fixing the data leakage, the values in this JSON file will change. 

Leave the corrected script at `/home/user/train_pipeline.py` and ensure the final correct metrics are written to `/home/user/metrics.json`.