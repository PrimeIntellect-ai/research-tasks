You are an AI assistant helping a data scientist clean datasets and set up an embedding evaluation pipeline. The environment is currently broken due to misconfigured services.

Your objective has two parts:
1. Fix and start the local services.
2. Write a Python script that perfectly implements a specific data cleaning and modeling pipeline.

### Part 1: Service Configuration
There are two services required for the pipeline:
1. A Redis cache.
2. A FastAPI embedding service located in `/app/api/`.

The embedding service uses a numerical backend to compute text embeddings and caches them in Redis. However, the service currently fails to run or connect. 
- You need to start the Redis server on the default port (6379).
- You need to configure and start the FastAPI service. The service code is in `/app/api/app.py`. It requires the environment variables `REDIS_HOST=127.0.0.1` and `OMP_NUM_THREADS=1` to function correctly without hanging the numerical backend. Start it on `127.0.0.1` port `8000`.

### Part 2: Data Cleaning and Modeling Pipeline
Write a standalone Python script at `/home/user/clean_pipeline.py`.
This script will be tested via standard input/output with thousands of random JSON payloads.

**Input Format:**
The script must read a single JSON array from `sys.stdin`. The array contains objects with `text` (string) and `target` (float).
Example: `[{"text": "  Hello, World!!! 123 ", "target": 0.5}, {"text": "Test.  ", "target": 1.2}]`

**Processing Steps:**
For each object in the array, maintain the original order:
1. **Clean the text**:
   - Strip leading and trailing whitespace.
   - Convert to lowercase.
   - Replace any character that is NOT a lowercase letter (a-z), digit (0-9), space ( ), period (.), or comma (,) with a single space.
   - Collapse any multiple consecutive spaces into a single space.
2. **Retrieve Embeddings**:
   - For each cleaned text, make a GET request to the local embedding service: `http://127.0.0.1:8000/embed?text=<cleaned_text_url_encoded>`
   - The API returns a JSON response: `{"embedding": [float, float, ...]}`. Extract the `embedding` list.
3. **Cross-Validation & Hyperparameter Tuning**:
   - Collect all embeddings into a 2D feature matrix `X` and targets into a 1D array `y`.
   - Use `sklearn.model_selection.KFold` with `n_splits=3` and `shuffle=False`.
   - Use `sklearn.linear_model.Ridge` regression to predict `y` from `X`.
   - Evaluate three alpha values: `[0.1, 1.0, 10.0]`.
   - For each alpha, calculate the average Mean Squared Error (MSE) across the 3 folds.
   - Select the `alpha` that yields the lowest average MSE. If there's a tie, select the smaller `alpha`.

**Output Format:**
Print a single JSON object to `sys.stdout` containing exactly these two keys:
- `optimal_alpha`: The chosen alpha (float).
- `cleaned_texts`: A list of the cleaned strings (in the original order).

Ensure your script is executable (`chmod +x`) and works deterministically. Do not print any debug information to stdout; stdout must contain *only* the final JSON object.