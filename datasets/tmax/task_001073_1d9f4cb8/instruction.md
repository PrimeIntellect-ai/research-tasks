You are tasked with normalizing and aggregating historical configuration states for our infrastructure. 

We have a set of raw configuration logs located in `/home/user/raw_configs/`. These logs track parameter changes across different servers. However, they are stored in an inefficient "wide" format, and the timestamp formatting is inconsistent.

Your goal is to write a Python script at `/home/user/process_configs.py` that reads all CSV files in `/home/user/raw_configs/`, processes them in parallel, and produces a single, normalized "long" format CSV file at `/home/user/normalized_configs.csv`.

**Data Processing Requirements:**
1. **Parallel Processing:** Your Python script must process the CSV files concurrently (e.g., using `multiprocessing` or `concurrent.futures.ProcessPoolExecutor`).
2. **Timestamp Parsing and Alignment:** 
   - The input files have a `Raw_Time` column with inconsistent formats (e.g., `YYYY-MM-DD HH:MM:SS` and `MM/DD/YYYY HH:MM:SS`). 
   - Parse these timestamps and align (floor) them to the nearest hour (e.g., `2023-01-01 10:45:30` becomes `2023-01-01 10:00:00`).
3. **Wide-to-Long Reshaping:**
   - The remaining columns represent server parameters in the format `<server_name>_<parameter_name>` (e.g., `web01_timeout`, `db01_workers`).
   - Reshape this data into a long format with columns: `aligned_hour`, `server_name`, `param_name`, and `param_value`.
4. **Aggregation:**
   - Because multiple configuration changes can occur within the same hour, aggregate the reshaped data by taking the **maximum** `param_value` for each unique combination of `aligned_hour`, `server_name`, and `param_name`.
   - Drop any rows where the original `param_value` was empty or NaN.

**Output Specification:**
The final output file must be saved to `/home/user/normalized_configs.csv`.
It must contain exactly four columns: `aligned_hour`, `server_name`, `param_name`, `param_value`.
The dates in `aligned_hour` must be formatted as `YYYY-MM-DD HH:00:00`.
The CSV must be sorted in ascending order by `aligned_hour`, then `server_name`, then `param_name`.
Include a standard CSV header.

Run your script to generate the final output file.