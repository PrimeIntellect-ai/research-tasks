You are an AI assistant helping a climate researcher organize and clean a messy dataset while properly tracking the data processing experiments. 

The researcher has a dataset located at `/home/user/raw_data.csv`. The dataset has three columns: `timestamp`, `temperature`, and `humidity`. 
The data has some issues:
1. `temperature` contains missing values (NaN/empty).
2. `humidity` contains impossible outlier values (sensors sometimes glitch and report values below 0% or above 100%).

Please perform the following end-to-end task:

1. **Environment & Service Setup:**
   - Install any necessary packages for data manipulation and experiment tracking (we recommend `pandas` and `mlflow`, but you may use any language/tools).
   - Start a local experiment tracking server (e.g., MLflow) running in the background. Bind it to `127.0.0.1` on port `5000`.

2. **Data Cleaning:**
   Write and execute a script that reads `/home/user/raw_data.csv` and applies the following operations:
   - Calculate the **median** of the valid `temperature` values.
   - Replace any missing (NaN) `temperature` values with this median.
   - Remove any rows where `humidity` is strictly less than `0` or strictly greater than `100`.
   - Save the cleaned dataset to `/home/user/cleaned_data.csv` (keep the header and original column order).

3. **Experiment Tracking:**
   In the same script, log this cleaning run to your local tracking server on port 5000. 
   - Use an experiment named exactly `climate_cleaning`.
   - Log a metric called `missing_imputed` (the integer number of missing temperature values that were replaced).
   - Log a metric called `rows_removed` (the integer number of rows that were dropped due to humidity outliers).
   
4. **Output Verification:**
   - After the script finishes successfully, write the unique Run ID of the tracked experiment to `/home/user/run_id.txt`.

Ensure your tracking server is still running at the end of the task so that the metrics can be verified programmatically via the server's API.