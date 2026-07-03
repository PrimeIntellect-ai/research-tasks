You are a machine learning engineer tasked with preparing a training dataset of sensor readings for a predictive maintenance model. The data is currently split across several CSV files and needs to be cleaned, feature-engineered, validated, and stored in an efficient format for large-scale training.

Your task is to build a reproducible pipeline. You need to create a Python script `/home/user/pipeline/prepare.py` and a bash script `/home/user/pipeline/run.sh` that executes the pipeline. 

Here are the detailed requirements:
1. You have three CSV files located in `/home/user/data/`: `data_1.csv`, `data_2.csv`, and `data_3.csv`. Each contains columns `id`, `sensor_A`, `sensor_B`, and `sensor_C`.
2. In `prepare.py`:
   - Load and concatenate all three CSV files into a single pandas DataFrame.
   - Sort the DataFrame by the `id` column in ascending order and reset the index.
   - Compute the rolling covariance over a window of 10 rows between `sensor_A` and `sensor_B` (name this new column `cov_AB`), and between `sensor_A` and `sensor_C` (name it `cov_AC`). The rolling window should calculate the covariance using the current row and the 9 preceding rows (e.g., using `pandas.Series.rolling(window=10).cov()`).
   - Validate the data by filtering out anomalies: drop any rows where `cov_AB` is strictly less than 0. Also, drop any rows that contain `NaN` values resulting from the rolling window computation.
   - Save the cleaned and feature-engineered DataFrame to `/home/user/data/prepared.parquet` using the Parquet format (which is optimized for large-scale data storage).
   - Calculate the Pearson correlation coefficient between the `cov_AB` and `cov_AC` columns on this final, filtered dataset. Round the result to exactly 4 decimal places.
   - Save this single rounded correlation value to a text file at `/home/user/pipeline/correlation.txt`.
3. In `run.sh`:
   - Write a bash script that installs any necessary Python packages (e.g., `pandas`, `pyarrow` or `fastparquet` for Parquet support) using `pip`.
   - Run the `prepare.py` script.
   - Ensure `run.sh` is executable (`chmod +x`).

The automated test will run `/home/user/pipeline/run.sh` and then verify the existence and contents of `/home/user/data/prepared.parquet` and `/home/user/pipeline/correlation.txt`.