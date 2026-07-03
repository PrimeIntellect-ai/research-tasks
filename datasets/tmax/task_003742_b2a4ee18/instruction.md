You are helping a researcher organize and process their experimental datasets. They have an ETL pipeline written in Python, but it has a few bugs related to data types and linear algebra, causing downstream reproducibility issues.

The researcher has provided the following files in `/home/user/data/`:
1. `raw.csv`: The raw experimental data containing features and a `batch_id`.
2. `meta.json`: A mapping of `batch_id` (as strings) to a `scaling_factor`.
3. `weights.csv`: A 3x3 transformation matrix.

The current pipeline script is located at `/home/user/etl_pipeline.py`. 

Your objectives are:
1. **Fix the Data Quality Bug:** The `raw.csv` file has missing values in the `batch_id` column. Because of this, pandas silently casts the column to float, which makes the downstream string conversion (e.g., `1.0` instead of `1`) fail to match the keys in `meta.json`. Modify the script to fill any missing `batch_id` values with `999` and ensure the column is properly treated as integers before being converted to strings to look up the scaling factor.
2. **Fix the Linear Algebra Bug:** The pipeline is currently performing element-wise multiplication between the feature matrix ($X$) and the weights matrix ($W$). Fix the code so it performs proper matrix multiplication ($X \times W$).
3. **Pipeline Output:** Ensure the fixed python script saves the processed data to `/home/user/output.csv` with the columns `sample_id,out1,out2,out3`.
4. **Reproducibility Testing:** Write a Bash script at `/home/user/test_reproducibility.sh` that runs `python3 /home/user/etl_pipeline.py` exactly 3 times. After each run, it should compute the MD5 checksum of `/home/user/output.csv` and append the standard `md5sum` output line to `/home/user/reproducibility_log.txt`.

Make sure your shell script is executable (`chmod +x`). Once you have fixed the Python script and created the Bash script, run the Bash script to generate the `reproducibility_log.txt`.