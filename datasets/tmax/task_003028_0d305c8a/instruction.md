You are a Data Analyst working on a text classification project. We have a Python script at `/home/user/workspace/train_pipeline.py` that processes a dataset (`/home/user/workspace/dataset.csv`). The script computes TF-IDF embeddings, applies dimensionality reduction, trains a Random Forest model, and logs the accuracy to MLflow.

However, a senior data scientist reviewed the code and noticed a major flaw: **data leakage**. The TF-IDF vectorizer and TruncatedSVD are being fitted on the *entire* dataset before the train-test split, meaning information from the test set is leaking into the training process. 

Your task is to fix this leakage and properly evaluate the model's performance:

1. **Fix the Data Leakage:** Modify `/home/user/workspace/train_pipeline.py`. Construct an `sklearn.pipeline.Pipeline` that chains the embedding computation (`TfidfVectorizer`), dimensionality reduction (`TruncatedSVD`), and the classifier (`RandomForestClassifier`). 
2. **Proper Evaluation:** Instead of a single train-test split, evaluate the entire pipeline using 5-fold cross-validation. Use `sklearn.model_selection.StratifiedKFold` with `n_splits=5`, `shuffle=True`, and `random_state=42`. 
3. **Compute Confidence Intervals:** Calculate the 95% confidence interval (CI) for the mean cross-validation accuracy. Use a Student's t-distribution (`scipy.stats.t.interval`) based on the 5 fold scores.
4. **Experiment Tracking:** Use MLflow in the script to log three metrics to an experiment named `"text_classification_fixed"`: 
   - `cv_mean` (the mean accuracy)
   - `ci_lower` (the lower bound of the 95% CI)
   - `ci_upper` (the upper bound of the 95% CI)
5. **JSON Output:** Save the calculated confidence intervals to `/home/user/workspace/ci_results.json` in the following exact format:
   ```json
   {
       "ci_lower": 0.1234,
       "ci_upper": 0.5678
   }
   ```
   (Round the values to 4 decimal places in the JSON file).

Make sure you install any required Python packages (e.g., `scikit-learn`, `pandas`, `mlflow`, `scipy`) using `pip`. The dataset is already provided, but you may need to initialize MLflow or just let it create the `mlruns` directory locally. Run your fixed script to ensure it generates the required JSON file and MLflow logs.