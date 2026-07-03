You are tasked with building a time-series data processing pipeline in Rust for a configuration management tracking system. We monitor "configuration drift" across multiple servers. Raw drift scores are recorded at regular intervals but are noisy. 

Your objective is to build a multi-stage pipeline that reads the raw data, computes rolling statistics to smooth the noise, normalizes the smoothed data, and generates alerts for significant configuration deviations.

Here are the requirements:

1. **Input Data**: 
   You will find a set of CSV files in `/home/user/drift_data/`. Each file is named `<server_name>.csv` (e.g., `server_alpha.csv`) and contains two columns: `timestamp` (integer) and `drift_score` (float).

2. **Data Transformation (Rust)**:
   Write a Rust program in a new project at `/home/user/drift_analyzer` that performs the following for each server's time series:
   - **Rolling Average**: Calculate a 3-step rolling average of the `drift_score`. For a given timestamp at index $i$ (where $i \ge 2$), the rolling average is the mean of the scores at $i$, $i-1$, and $i-2$. Drop the first two data points (index 0 and 1) from the resulting series, as they do not have a full 3-step window.
   - **Standardization**: Calculate the population mean ($\mu$) and population standard deviation ($\sigma$) of the *rolling averages* for that specific server. Then, convert each rolling average into a Z-score: $Z = (x - \mu) / \sigma$.

3. **Alert Generation**:
   - Filter the standardized results. Keep only the data points where the Z-score is strictly greater than `1.5`.
   - Round the Z-score to exactly 3 decimal places (e.g., `1.543`).

4. **Output Format**:
   - The Rust program must output the final alerts to a JSON file at `/home/user/alerts.json`.
   - The JSON must be an object where keys are the server names (without the `.csv` extension, e.g., `"server_alpha"`), and values are arrays of objects containing the `timestamp` and the rounded `z_score`.
   - Example format:
     ```json
     {
       "server_alpha": [
         {"timestamp": 104, "z_score": 1.621}
       ],
       "server_beta": []
     }
     ```

5. **Orchestration**:
   Create a bash script at `/home/user/run_pipeline.sh` that:
   - Compiles the Rust program for a release build.
   - Executes the compiled Rust program to process `/home/user/drift_data/` and produce `/home/user/alerts.json`.
   Make sure the script is executable (`chmod +x`).

Notes:
- Use standard, exact mathematical formulas for population mean and population standard deviation.
- Do not round intermediate calculations; only round the final Z-score before writing to JSON.
- If a server's standard deviation is exactly 0, no alerts should be generated for it (avoid division by zero).