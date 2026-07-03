You are a Machine Learning Engineer preparing training data and evaluating models for a new text classification pipeline. We have a local embedding service that hosts two candidate embedding models, but we don't know which one has better inference performance. 

Your task is to benchmark the models, use the faster one to compute features, and train a baseline classifier.

Here are your instructions:

1. **Start the API Service:**
   There is a Flask API script located at `/home/user/service.py`. It requires `flask` (you may need to install it). Start this service in the background. It will run on `http://127.0.0.1:5000` and exposes two endpoints: `/embed/model_alpha` and `/embed/model_beta`. Both accept POST requests with JSON payload `{"text": "your text here"}` and return `{"embedding": [float, float, ...]}`.

2. **Inference Performance Benchmarking:**
   Write a Bash script at `/home/user/benchmark.sh` that sends 50 sequential requests to each endpoint (using any arbitrary text) and calculates the total time taken for each model. 
   Determine which model is faster based on this benchmark.

3. **Embedding Computation & Feature Engineering:**
   You are provided with a training dataset at `/home/user/dataset.csv` containing `id`, `text`, and `label`.
   Write a Python script (`/home/user/train.py`) that:
   - Reads the CSV.
   - Fetches the embedding for each `text` using *only the faster endpoint* you identified.
   - Combines the resulting embedding array with the length of the original text (number of characters) as an additional engineered feature. (e.g., if the embedding has 5 dimensions, your final feature vector for each row should have 6 dimensions: `[emb1, emb2, emb3, emb4, emb5, text_length]`).

4. **Model Training and Evaluation:**
   - In the same Python script, split your engineered features and labels into training and testing sets using `sklearn.model_selection.train_test_split` with `test_size=0.25`, `random_state=42`, and `shuffle=False`.
   - Train a `sklearn.linear_model.LogisticRegression` with `random_state=42` on the training set.
   - Evaluate the accuracy on the test set.

5. **Reporting:**
   Generate a final report at `/home/user/report.json` with exactly the following structure:
   ```json
   {
       "faster_model": "model_alpha", // or "model_beta"
       "test_accuracy": 0.85 // your computed accuracy as a float
   }
   ```

Constraints:
- You must use multi-language approaches: Bash for the benchmark script (`/home/user/benchmark.sh`) and Python for the ML pipeline (`/home/user/train.py`).
- Do not modify `service.py` or `dataset.csv`.