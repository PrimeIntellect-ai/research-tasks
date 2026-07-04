You are a Machine Learning Engineer preparing training data and validating a nearest-neighbor recommendation algorithm. 

Your task is to implement a multi-language pipeline (Python and Bash) to clean raw feature data, compute similarity recommendations, and validate the output against a legacy baseline model.

**Step 1: Data Cleaning (Python)**
You have a raw dataset located at `/home/user/features.csv`. The file has headers: `id,f1,f2,f3`.
Some columns contain missing values (empty strings) and extreme outliers. 
Write a Python script `/home/user/clean.py` that reads this file and performs the following operations strictly in this order:
1. **Missing Value Handling**: Impute missing values in each feature column (`f1`, `f2`, `f3`) with the *mean* of the present values in that specific column.
2. **Outlier Handling**: Cap all feature values to be within the range `[-10.0, 10.0]`. Any value `< -10.0` becomes `-10.0`, and any value `> 10.0` becomes `10.0`.
3. Save the cleaned dataset to `/home/user/clean_features.csv` (keeping the same headers and `id` column, formatting floats to 4 decimal places).

**Step 2: Similarity Search (Python)**
Write a Python script `/home/user/recommend.py` that reads `/home/user/clean_features.csv`.
For each item, find its top 2 nearest neighbors using **Euclidean distance** based on the features `f1, f2, f3`. An item cannot be its own neighbor.
Save the results to `/home/user/nn_results.csv` with headers `id,nn1_id,nn2_id` (where `nn1_id` is the closest, and `nn2_id` is the second closest). If distances are exactly equal, break ties by sorting the `id` strings alphabetically.

**Step 3: Model Output Validation (Bash)**
A legacy baseline recommendation file is provided at `/home/user/baseline_nn.csv` (same format: `id,nn1_id,nn2_id`).
Write a Bash script `/home/user/evaluate.sh` that validates your new algorithm against the baseline. The script must:
1. Read both `/home/user/nn_results.csv` and `/home/user/baseline_nn.csv`.
2. For each `id`, check if the *set* of the top 2 neighbors exactly matches between the two files (ignoring the order: e.g., if new gives `B, C` and baseline gives `C, B`, that is a match).
3. Calculate the accuracy (number of exact set matches divided by total number of items).
4. Output *only* the final accuracy as a float to 2 decimal places (e.g., `0.80`) to the file `/home/user/accuracy.txt`.

Ensure all scripts are executable. Run your pipeline so that `/home/user/clean_features.csv`, `/home/user/nn_results.csv`, and `/home/user/accuracy.txt` are generated.