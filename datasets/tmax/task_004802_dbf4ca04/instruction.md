You are an AI assistant acting as a Data Scientist. We have a pipeline that cleans messy text data, extracts embeddings, trains a simple regression model, and serves predictions. 

However, the pipeline is currently broken, and the previous engineer left it in an unfinished state. Your task is to complete the following workflow:

1. **Fix and Install the Vendored Package**:
   There is a custom internal package vendored at `/app/text-cleaner-pro`. It contains two main functions you need: `clean_text(text)` and `get_embedding(text)` from `text_cleaner_pro.core`.
   The package has a deliberate bug introduced recently that prevents the embeddings from working (it returns an empty array or crashes). Find the perturbation in the package source, fix it, and install the package into your Python environment.

2. **Clean Data and Train Model**:
   You have a dataset at `/home/user/data/messy_data.csv` with columns: `id`, `text`, and `target` (a continuous float variable).
   - Read the dataset.
   - Use `clean_text` on the `text` column.
   - Use `get_embedding` to convert the cleaned text into feature vectors.
   - Train a standard Ridge Regression model (from `scikit-learn`, with default parameters `alpha=1.0`) on the embeddings to predict `target`.
   - Track your experiment by computing the Mean Squared Error (MSE) on the training set. Save this metric to a JSON file at `/home/user/experiment_results.json` in the format: `{"train_mse": <float>}`.

3. **Serve the Model (API)**:
   Create and run a web server (you can use Flask or FastAPI) that listens exactly on `127.0.0.1:8080`.
   - Expose a `POST` endpoint at `/predict`.
   - The endpoint must require an authorization header: `X-API-Key: DS-CLEAN-2024`. Reject requests without this valid key with a 401 or 403 status.
   - The endpoint should accept a JSON payload: `{"text": "<raw input string>"}`.
   - The endpoint should return a JSON response: `{"cleaned_text": "<string>", "prediction": <float>}`.
   - Keep the server running in the foreground or as a background process so it can be queried.

Write the necessary scripts in Python. Ensure your server is running and listening on port 8080 before you complete the task.