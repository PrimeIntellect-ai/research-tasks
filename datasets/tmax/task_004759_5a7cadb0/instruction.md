You are an Machine Learning Engineer preparing a data pipeline and inference script for a new model. Your task involves setting up the local service environment, fixing a subtle data processing bug, and reconstructing the model for local inference.

**Step 1: Environment Setup**
We have two services defined in `/home/user/services/docker-compose.yml`:
1. `metadata_store`: A Redis instance holding preprocessing hyperparameters.
2. `model_repo`: A simple Nginx server hosting the model architecture and weights.

Currently, the `docker-compose.yml` is misconfigured (ports are mismatched and networks are isolated). 
Fix the `docker-compose.yml` so that:
- `metadata_store` is exposed to the host on port 6379.
- `model_repo` is exposed to the host on port 8080.
Start the services using Docker Compose. 

**Step 2: Model Reconstruction & Data Processing**
Write a Python script at `/home/user/cli.py`. This script will act as a CLI for data processing and inference.
The script must:
1. Read a JSON array of dictionaries from Standard Input (`stdin`). Each dictionary represents a row of training data with keys `item_id` (integer or null) and `feature_val` (float).
2. Fetch the preprocessing hyperparameters from the `metadata_store` (Redis on localhost:6379). Read the string value at key `preprocessing_config` and parse it as JSON. It contains a `fill_value` integer.
3. Convert the input data into a pandas DataFrame. 
4. **Critical Fix:** You must impute any missing (null) values in the `item_id` column using the `fill_value` fetched from Redis. *Beware:* standard pandas operations often silently cast integer columns with missing values to floats (introducing `NaN`). The model strictly requires `item_id` to be of integer type (e.g., standard Python `int` or pandas `Int64` without decimals). If it is passed as a float, the model will produce incorrect bit-level results.
5. Download the model architecture (`arch.py`) and weights (`weights.pkl`) from `http://localhost:8080/`. Dynamically load the `Model` class from `arch.py`, instantiate it, and load the weights.
6. Pass the processed `item_id` (as integers) and `feature_val` columns to the model's `predict(item_ids: list[int], feature_vals: list[float]) -> list[float]` method.
7. Print the resulting list of float predictions to Standard Output (`stdout`) as a JSON array, with no other text.

Ensure `/home/user/cli.py` is executable and prints only the final JSON array.