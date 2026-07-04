You are an AI assistant acting as a Machine Learning Engineer preparing a robust training pipeline and dataset.

Your environment is an Ubuntu Linux system. You have sudo-less access. Python 3 is installed.

Here is your objective:
You need to clean a raw text dataset using embedding-based deduplication, train a model with hyperparameter tuning, and benchmark its inference speed via a local API.

**Phase 1: Dataset Preparation (Embedding & Retrieval)**
1. A raw dataset exists at `/home/user/raw_data.csv` with columns `text` and `label`.
2. Install `pandas` and `scikit-learn`.
3. Write a Python script to deduplicate the dataset based on semantic similarity using TF-IDF.
    - Fit a `TfidfVectorizer(stop_words='english')` on the entire `text` column of the raw dataset.
    - Iterate through the dataset sequentially (from index 0 to the end).
    - Keep the first row. For each subsequent row, compute its cosine similarity against all *previously kept* rows.
    - If the row has a cosine similarity `>= 0.80` with ANY previously kept row, discard it. Otherwise, keep it.
    - Save the resulting dataset to `/home/user/cleaned_data.csv` (keep the same columns).

**Phase 2: Model Training & Cross-Validation**
1. Using `/home/user/cleaned_data.csv`, train a text classification model pipeline.
2. The pipeline should consist of a `TfidfVectorizer(stop_words='english')` and a `LogisticRegression(random_state=42, solver='liblinear')`.
3. Perform 3-fold Cross-Validation using `GridSearchCV` to tune the `C` parameter of the Logistic Regression model. Test the values `C = [0.1, 1.0, 10.0]`. Use accuracy as the metric.
4. Save the single best `C` value as a float (e.g., `1.0`) to a text file at `/home/user/best_param.txt`.
5. Save the best fitted pipeline model to `/home/user/model.joblib`.

**Phase 3: Inference API & Benchmarking**
1. Install `flask`. Write a Flask application at `/home/user/app.py` that loads `/home/user/model.joblib`.
2. Expose a POST endpoint `/predict` that accepts a JSON payload `{"text": "your text here"}` and returns a JSON response `{"prediction": "predicted_label"}`.
3. Start the Flask server on port `5000` in the background.
4. Write a Bash script `/home/user/benchmark.sh` that sends 50 sequential POST requests to the `/predict` endpoint using `curl`. Use the payload `{"text": "Is this a valid test message?"}`. 
5. The bash script must measure the total time taken to execute all 50 requests and write the total time in seconds (just the number) to `/home/user/benchmark_results.txt`. Execute this script.

Ensure all output files (`cleaned_data.csv`, `best_param.txt`, `model.joblib`, `app.py`, `benchmark.sh`, `benchmark_results.txt`) are located exactly in `/home/user/`.