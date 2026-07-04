You are a Data Engineer building a data quality testing suite for an ETL pipeline. We need to verify that the raw product descriptions flowing through the pipeline contain enough signal for our downstream machine learning classification models.

We have a sample of 100 raw product records in JSON lines format at `/home/user/data/raw_products.jsonl`. Each line is a JSON object with `id`, `description`, and `category`.

Your task is to write a script in the language of your choice (Python with `scikit-learn` is recommended) that performs an end-to-end data quality test:

1. **Read Data**: Load the 100 records from `/home/user/data/raw_products.jsonl`. Maintain the original order.
2. **Embedding Computation**: Extract the `description` fields and compute TF-IDF embeddings using scikit-learn's `TfidfVectorizer` (or equivalent). Configure the vectorizer to use English stop words (`stop_words='english'`) and limit to the top 50 features (`max_features=50`).
3. **Model Training and Evaluation**: 
   - Split the data into training and testing sets. Use the first 80 records for training and the remaining 20 records for testing.
   - Train a default `LogisticRegression` classifier (random_state=42) on the training embeddings to predict the `category`.
   - Generate predictions on the 20 testing embeddings.
   - Calculate the accuracy of the predictions.
4. **Model Output Validation**: Write the test results to `/home/user/test_results.json` strictly in the following JSON format:
```json
{
  "accuracy": 1.0,
  "passed": true,
  "predictions": ["CategoryA", "CategoryB", "..."]
}
```
*Note*: `passed` should be a boolean that is `true` if accuracy is greater than `0.80`, and `false` otherwise. `predictions` must be a list of 20 strings representing the predicted categories for the test set in order.

You may use any language, but you must create the `/home/user/test_results.json` file exactly as specified.