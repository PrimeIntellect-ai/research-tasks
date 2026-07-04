You are a data engineer building an ETL pipeline to process product descriptions and train a baseline classification model. 

Your task is to write a Python script at `/home/user/pipeline.py` that performs the following steps:

1. **Package Installation**: Ensure `pandas`, `scikit-learn`, and `pydantic` are installed.
2. **Data Schema Enforcement**: Read the CSV file located at `/home/user/products.csv`. Validate the data using a `pydantic` model. The expected schema is:
   - `product_id`: integer
   - `text`: string
   - `label`: string
   Drop any rows that fail validation.
3. **Embedding Computation**: Use `sklearn.feature_extraction.text.TfidfVectorizer` to extract features from the valid `text` column. Set `max_features=500` and `stop_words='english'`.
4. **Dimensionality Reduction**: Reduce the dimensionality of the TF-IDF features using `sklearn.decomposition.TruncatedSVD`. Set `n_components=20` and `random_state=42`.
5. **Cross-validation and Hyperparameter Tuning**: Train a `sklearn.linear_model.LogisticRegression` (with `random_state=42`) to predict the `label` using the reduced features. Use `sklearn.model_selection.GridSearchCV` with 3-fold cross-validation (`cv=3`) to find the best `C` parameter from the grid `[0.1, 1.0, 10.0]`.
6. **Reporting**: Save the best `C` value and its mean cross-validated score to `/home/user/model_results.json` in the exact format:
   ```json
   {
       "best_C": 1.0,
       "best_score": 0.85
   }
   ```
   (Replace `1.0` and `0.85` with the actual computed values).

Run the script so that the `/home/user/model_results.json` is generated.