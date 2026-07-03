You are an MLOps engineer tracking experiment artifacts for a recommendation system. A daily data pipeline script at `/home/user/pipeline.py` merges user data with transaction data to generate candidate items for similarity search.

However, the downstream reproducibility tests are failing. The `item_id` column in the generated `output.csv` is silently being converted to floats (e.g., `101.0` instead of `101`) because some users have no transactions, which introduces `NaN` values and casts the entire column to `float64`. The downstream similarity search requires exact integer representations for valid lookups.

Your tasks are to:
1. Fix `/home/user/pipeline.py` so that the `item_id` column retains an integer representation in the output CSV (i.e., it should output `101` instead of `101.0`), while still preserving the rows for users with missing items (the missing items should remain empty in the CSV). You must use pandas' built-in nullable integer data type.
2. Run the fixed script to generate `/home/user/output.csv`.
3. We have past experiment artifacts stored in `/home/user/archive/`. Identify which of the CSV files in this directory suffer from the same silent float conversion bug in the `item_id` column.
4. Write the exact filenames (just the basenames, e.g., `run_1.csv`) of the corrupted artifacts to `/home/user/corrupt_artifacts.txt`, one filename per line.

Do not remove any users from the dataset when fixing the pipeline.