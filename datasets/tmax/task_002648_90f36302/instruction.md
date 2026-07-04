You are a data engineer building a test suite for an automated ETL pipeline that updates a recommendation system. 

We have an existing ETL script at `/home/user/src/run_etl.py`. This script reads raw interaction data, performs random projections to compute an item-item similarity matrix, and updates a Bayesian model with new click-through rate (CTR) posteriors (using a Beta-Binomial conjugate model). 

The ETL script reads an environment variable `ETL_SEED` to set its random seed.

Your task is to write a Python testing script at `/home/user/tests/validate_etl.py` and run it to produce a final validation report. The script must do the following:

1. **Pipeline Reproducibility Testing**: Run `/home/user/src/run_etl.py` twice via subprocess, setting `ETL_SEED=42` both times. Verify that the two runs produce exactly the same outputs. The ETL script outputs two files in `/home/user/output/`:
    - `similarity.npy` (a NumPy 2D array of item-item similarities)
    - `posteriors.json` (a JSON dictionary mapping `item_id` (string) to `{"alpha": float, "beta": float}`)

2. **Linear Algebra & Model Validation**: Load the `similarity.npy` matrix from the first run. 
    - Verify that the matrix is perfectly symmetric.
    - Find the top 3 most similar items to item index `0` (excluding item `0` itself). Assume the index in the matrix corresponds to the integer `item_id`.

3. **Bayesian Inference Validation**: Load `posteriors.json`. 
    - For each item, compute the expected posterior Click-Through Rate (CTR). For a Beta distribution, the expected value is `alpha / (alpha + beta)`.
    - Identify the integer `item_id` with the highest expected posterior CTR.

4. **Reporting**: Your script must generate a JSON file at `/home/user/test_report.json` with the exact following keys:
    - `"is_reproducible"`: (boolean) True if the files from the two runs are exactly identical.
    - `"is_symmetric"`: (boolean) True if the similarity matrix is exactly symmetric (`A == A.T`).
    - `"top_3_similar_to_0"`: (list of 3 integers) The integer indices of the top 3 items most similar to item `0`, ordered from most similar to least similar.
    - `"highest_ctr_item"`: (integer) The integer `item_id` of the item with the highest expected posterior CTR.
    - `"highest_ctr_value"`: (float) The expected posterior CTR value of that item, rounded to 4 decimal places.

Run your script to ensure `/home/user/test_report.json` is successfully created. You may install any necessary packages (e.g., `numpy`) using `pip`.