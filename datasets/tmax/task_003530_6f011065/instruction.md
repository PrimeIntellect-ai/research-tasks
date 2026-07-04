You are an AI assistant helping a DevOps team analyze configuration drift across two critical servers: Server Alpha and Server Beta. The configuration management system tracks key parameters over time and exports them as daily snapshots.

Your task is to write a Python script at `/home/user/analyze_drift.py` that processes these exported logs, calculates the configuration drift (distance) between the servers over time, computes summary statistics, and logs the pipeline execution.

**Input Data:**
You have two files located in `/home/user/data/`:
1. `/home/user/data/server_alpha.csv` - Encoded in `UTF-8`.
2. `/home/user/data/server_beta.csv` - Encoded in `UTF-16LE`.

Both CSV files have the same structure with a header row:
`date,cache_size,timeout,max_workers`
The `date` is in `YYYY-MM-DD` format. The other three columns are integer configuration values.

**Processing Requirements:**
1. **Character Encoding:** Your script must read both files using their correct encodings.
2. **Distance Computation:** For every date that exists in *both* files, calculate the configuration drift as the **Euclidean distance** between the 3-dimensional configuration vectors `[cache_size, timeout, max_workers]`.
3. **Summary Statistics:** Calculate the `min`, `max`, and `mean` (average) of these daily Euclidean distances. 
4. **Pipeline Logging:** Use Python's built-in `logging` module to log the pipeline execution to `/home/user/pipeline.log`. The log format must be exactly: `%(asctime)s - %(levelname)s - %(message)s`. 
   - Log `INFO - Pipeline STARTED` at the beginning.
   - Log `INFO - Successfully parsed input files` after reading.
   - Log `INFO - Pipeline COMPLETED` at the end.
5. **Output:** Write the summary statistics to a JSON file at `/home/user/drift_summary.json` with the exact following keys:
   - `"min_drift"` (float, rounded to 4 decimal places)
   - `"max_drift"` (float, rounded to 4 decimal places)
   - `"mean_drift"` (float, rounded to 4 decimal places)

Once your script is written, execute it so that the output files are generated.