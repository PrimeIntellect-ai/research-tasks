You are helping a research scientist organize and extract datasets from an SQLite database. 

The researcher has an SQLite database located at `/home/user/research.db`. Recently, the system suffered a power failure, and the researcher suspects that some database indices have become corrupted, occasionally returning stale or missing rows. Furthermore, their extraction queries are running too slowly.

Your task is to write and execute a Python script at `/home/user/process_research.py` that performs the following steps:

1. **Fix Corruption**: Connect to `/home/user/research.db` and repair all indices in the database using the appropriate SQLite command.
2. **Optimize**: Design and create a new covering index named `idx_opt_samples` on the `samples` table to optimize the extraction query (you must determine the best columns to index based on the query requirements).
3. **Query**: Write a complex SQL query to extract data based on these precise rules:
   - Find the top 3 `experiments.name` based on the total sum of `samples.measurement`.
   - Only include samples where the `sensors.sensor_type` is exactly `'TypeA'`.
   - Only include experiments where the `experiments.year` is `2023`.
   - The tables are:
     - `experiments` (`id`, `name`, `year`)
     - `sensors` (`id`, `sensor_type`)
     - `samples` (`id`, `exp_id`, `sensor_id`, `measurement`)
4. **Export**: The script must execute this query and export the results to `/home/user/results.json`.
   - The output must be a valid JSON array containing exactly 3 objects.
   - Each object must have exactly two keys: `"experiment_name"` (string) and `"total_value"` (float, rounded to 2 decimal places).
   - The array must be ordered by `"total_value"` in descending order.

Write the Python script, run it, and ensure `/home/user/results.json` is generated correctly.