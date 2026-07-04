You are tasked with fixing a broken data processing pipeline, training a bootstrapped ensemble model, and serving it via a REST API.

**Background:**
We use a vendored version of the `pyjanitor` library (located in `/app/pyjanitor`) for our data cleaning pipeline. A previous developer attempted to optimize the `fill_empty` function but introduced a bug. Now, when `fill_empty` is called to replace missing values in integer columns, it silently introduces `np.nan`, coercing the entire column into `float64` instead of preserving the integer type.

**Step 1: Fix the Vendored Package**
1. Inspect the vendored `pyjanitor` package in `/app/pyjanitor`. Locate the `fill_empty` implementation (typically in `janitor/functions/fill.py`).
2. Fix the bug so that it correctly fills missing values with the provided fill value without coercing integer columns to floats unnecessarily.
3. Install this fixed package into your Python environment.

**Step 2: Data Cleaning & Bootstrap Modeling**
1. Read the dataset at `/home/user/train_data.csv`. 
2. Use the fixed `pyjanitor` to fill all missing values in the dataset with `0`. Ensure that no columns that were originally integers (aside from the missing values) are converted to floats.
3. The dataset has a target column `target`. All other columns are features.
4. Using `sklearn.neural_network.MLPRegressor`, train an ensemble of **10** models. 
   - Architecture for each model: `hidden_layer_sizes=(32, 16)`, `activation='relu'`, `max_iter=500`.
   - Each model must be trained on a distinct bootstrap sample (sampled with replacement, same size as the original dataset). Use `random_state=i` for the sampling and the MLPRegressor initialization, where `i` ranges from 0 to 9 for the 10 models.

**Step 3: Serve the Model**
Create a web server (e.g., using Flask or FastAPI) to serve predictions from your ensemble.
- **Listen on:** `0.0.0.0` port `8000`
- **Authentication:** All requests must include the header `Authorization: Bearer secret-ds-token-8819`
- **Endpoint:** `POST /predict`
- **Input:** JSON object containing key-value pairs of features. (e.g., `{"feature_1": 10, "feature_2": 5, ...}`)
- **Output:** JSON object containing:
  - `mean_prediction`: The mean of the predictions from the 10 models (float).
  - `uncertainty`: The standard deviation of the predictions from the 10 models (float, sample standard deviation, ddof=1).

Run the server in the background and leave it running. You may test it via curl. Once you have validated the endpoint works as specified, leave the process running.