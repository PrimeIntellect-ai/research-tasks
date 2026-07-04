You are a data analyst working with a dataset of sensor readings. You have been given a set of CSV files and a simple linear model. 

Your task is to write a robust Bash script at `/home/user/process.sh` that performs model inference, calculates statistical metrics, and proves pipeline reproducibility.

**Input Data:**
1. A directory `/home/user/data/` contains several CSV files (e.g., `sensor_batch_1.csv`, `sensor_batch_2.csv`, etc.). Each CSV has a header: `sensor_A,sensor_B,actual_output`.
2. A model configuration file at `/home/user/model_params.txt` containing the weights for a linear model in the format:
   ```
   weight_A=1.5
   weight_B=-0.5
   bias=2.0
   ```

**Requirements for `/home/user/process.sh`:**
1. **Model Inference**: The script must read all CSV files in `/home/user/data/` (ignoring headers during calculation) and calculate a predicted value for each row using the formula:
   `predicted_output = (sensor_A * weight_A) + (sensor_B * weight_B) + bias`
2. **Statistical Analysis**: Using the combined predictions and actual outputs from all CSV files, calculate the Covariance and the Pearson Correlation Coefficient between `predicted_output` and `actual_output`. 
3. **Formatting**: The script must output these exact two lines to `/home/user/metrics.txt`:
   ```
   Covariance: <value rounded to 4 decimal places>
   Correlation: <value rounded to 4 decimal places>
   ```
4. **Reproducibility Testing**: Your bash script must be deterministic. At the end of `/home/user/process.sh`, run the inference and statistics pipeline twice, saving the `metrics.txt` file each time. Calculate the MD5 checksum of the `metrics.txt` file and save the checksum (just the hash and filename, standard `md5sum` output) to `/home/user/reproducibility.txt` to prove the pipeline yields identical results on repeated runs.

Make sure your script is executable (`chmod +x /home/user/process.sh`) and run it so the output files are generated. You may use standard Linux tools (awk, bash, grep) and Python 3 if needed within your Bash script.