You are a data engineer tasked with fixing a broken ETL and inference pipeline. 

In `/home/user/pipeline/`, you will find several files:
- `data_A.csv`: Contains `user_id` and `feature_1` (float).
- `data_B.csv`: Contains `user_id` and `feature_2` (large integers representing exact, high-precision counts).
- `labels.csv`: Ground truth labels for each `user_id`.
- `etl.py`: A pandas script that merges `data_A` and `data_B`, then outputs to `processed.csv`.
- `score.py`: A script that reads `processed.csv` and `labels.csv` to calculate the Mean Squared Error (MSE) of a simple linear regression formula (`prediction = feature_1 + feature_2`).

**The Problem:**
The current `etl.py` script performs a left join. Because some users in `data_A` are missing from `data_B`, `NaN` values are introduced into `feature_2`. Pandas silently casts the entire `feature_2` column to `float64`. Since `feature_2` contains integers larger than $2^{53}$, this float conversion causes a loss of numerical precision. Downstream, this precision loss causes the inference MSE to be higher than it should be.

**Your Tasks:**
1. **Fix the Pipeline:** Modify `/home/user/pipeline/etl.py` to preserve exact integer precision for `feature_2`. Fill any missing values in `feature_2` with `0`. You must use a nullable integer data type in pandas (e.g., `Int64`) to prevent the silent float conversion during the merge. The script should still output the fixed data to `/home/user/pipeline/processed.csv`.
2. **Correlation Analysis:** Create a new Python script `/home/user/pipeline/analysis.py` that reads the fixed `processed.csv` and calculates the Pearson correlation coefficient between `feature_1` and `feature_2`. Save only the numeric float value, rounded to 4 decimal places, to `/home/user/pipeline/correlation.txt`.
3. **Accuracy Testing:** Run the provided `/home/user/pipeline/score.py` on your fixed dataset. It will print the MSE. Save the resulting MSE value to `/home/user/pipeline/mse.txt`.
4. **Reproducibility:** Create a shell script `/home/user/pipeline/run_pipeline.sh` that runs `etl.py`, `analysis.py`, and `score.py` in sequence.

Ensure that the final output files (`processed.csv`, `correlation.txt`, `mse.txt`, and `run_pipeline.sh`) are correctly formatted and located in `/home/user/pipeline/`.