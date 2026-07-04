You are a data analyst tasked with processing a batch of product reviews to predict missing categories using a Bayesian approach and benchmark the inference performance. 

You have been provided with a dataset at `/home/user/reviews.csv`. The dataset is supposed to contain three columns: `review_id`, `text`, and `category`. The `category` is either 'electronics', 'books', or missing (empty string). 

Perform the following steps using Python:

1. **Schema Enforcement & Cleaning:** Read `/home/user/reviews.csv`. Filter out any rows that violate this schema:
   - `review_id` must be convertible to an integer.
   - `text` must be a non-empty string.
   Keep only the valid rows for the next steps.

2. **Embedding / Vectorization:** Compute TF-IDF embeddings for the `text` column of the cleaned dataset. 
   - Use `sklearn.feature_extraction.text.TfidfVectorizer`.
   - Set `stop_words='english'` and `max_features=50`.
   - Fit the vectorizer on the entire cleaned text column (both known and unknown categories) and transform it into a feature matrix.

3. **Bayesian Inference:** 
   - Separate the cleaned data into a labeled set (where `category` is 'electronics' or 'books') and an unlabeled set (where `category` is missing or empty).
   - Train a Multinomial Naive Bayes classifier (`sklearn.naive_bayes.MultinomialNB` with default parameters) using the TF-IDF features of the labeled set as inputs and the `category` as the target.
   - Predict the class probabilities for the unlabeled set. 

4. **Inference Benchmarking:** 
   - Isolate the `.predict_proba()` call on the unlabeled feature matrix.
   - Run this specific prediction call 100 times in a loop.
   - Calculate the average time taken per call (in seconds).
   - Save this metric to `/home/user/benchmark.json` in the exact format: `{"avg_inference_time_sec": 0.00123}` (replace with your calculated float).

5. **Output Predictions:**
   - Save the predictions for the unlabeled set to `/home/user/predictions.csv`.
   - The CSV must have exactly three columns: `review_id`, `prob_books`, `prob_electronics`.
   - `prob_books` and `prob_electronics` should be the float probabilities output by the Naive Bayes model.
   - Sort the CSV by `review_id` in ascending order.