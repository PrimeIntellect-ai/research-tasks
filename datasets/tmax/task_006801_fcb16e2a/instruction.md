You are an MLOps engineer tracking hyperparameter tuning artifacts. You have a directory of experiment logs, but the data is messy, and you need to build a pipeline to validate, process, and analyze it.

In `/home/user/experiments/`, there are several JSON files representing individual training runs. Your task is to build a Python script (and use any standard bash tools) to perform the following pipeline:

1. **Schema Enforcement (ETL)**: Read all JSON files in `/home/user/experiments/`. Keep only the files that strictly contain the following keys and correct types. Discard any files that are missing keys, contain extra keys, or have incorrect types.
   - `run_id` (string)
   - `learning_rate` (float)
   - `batch_size` (int)
   - `num_layers` (int)
   - `metrics` (dictionary containing strictly a `val_accuracy` float key)

2. **Embedding & Retrieval**: Represent each valid experiment's hyperparameters as a 3-dimensional vector: `[learning_rate, batch_size, num_layers]`.
   - Apply Min-Max scaling to each feature independently across the *valid* dataset (so the minimum value becomes 0.0 and maximum becomes 1.0).
   - We want to deploy a new model with the target configuration: `{"learning_rate": 0.005, "batch_size": 64, "num_layers": 3}`.
   - Scale this target configuration using the exact same min-max bounds computed from the dataset.
   - Calculate the Euclidean distance between the scaled target configuration and all valid scaled experiment configurations.
   - Save the `run_id`s of the **top 3 closest** experiments (smallest distance), sorted by distance ascending, as a JSON array of strings in `/home/user/closest_runs.json`.

3. **Hyperparameter Aggregation**: To simulate a cross-validation summary, group the valid experiments by their `(batch_size, num_layers)` pairs.
   - Calculate the mean `val_accuracy` for each unique pair.
   - Identify the pair with the highest mean `val_accuracy`.
   - Write this to `/home/user/best_hyperparams.txt` in the exact format: `batch_size,num_layers,mean_accuracy` (where mean_accuracy is rounded to exactly 4 decimal places). If there is a tie, pick the one with the highest `batch_size`.

Note: You can write a single Python script (e.g., `/home/user/process.py`) to handle this logic. Use standard libraries (e.g., `json`, `math`).