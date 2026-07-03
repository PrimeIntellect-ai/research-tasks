You are an AI assistant helping a data analyst debug a machine learning script. 

The analyst has written a script located at `/home/user/train.py` that reads a dataset of text reviews from `/home/user/reviews.csv` and trains a Logistic Regression model using TF-IDF features to predict sentiment. The script uses `GridSearchCV` to find the best hyperparameter `C` for the model.

However, the analyst realized there is a fundamental methodological flaw in their code: **data leakage**. They are applying `fit_transform` with the `TfidfVectorizer` to the entire dataset *before* performing cross-validation, meaning information from the validation folds is leaking into the training folds.

Your task is to rewrite `/home/user/train.py` to fix this issue and perform a proper hyperparameter search:
1. Fix the data leakage by creating a scikit-learn `Pipeline` that chains the `TfidfVectorizer` (name the step `'tfidf'`) and `LogisticRegression(random_state=42)` (name the step `'clf'`).
2. Use `GridSearchCV` with 3-fold cross-validation (`cv=3`) to evaluate the pipeline.
3. Tune the following hyperparameters:
   - For the vectorizer: `tfidf__max_features` with values `[10, 50]`
   - For the classifier: `clf__C` with values `[0.1, 1.0]`
4. After fitting the grid search on the dataset (`X = df['text']`, `y = df['sentiment']`), output the best cross-validation score and the best parameters to a JSON file at `/home/user/results.json`.

The resulting `/home/user/results.json` should have the following exact structure:
```json
{
  "best_score": 0.85,
  "best_params": {
    "clf__C": 1.0,
    "tfidf__max_features": 50
  }
}
```

Run your script to ensure the JSON file is generated correctly.