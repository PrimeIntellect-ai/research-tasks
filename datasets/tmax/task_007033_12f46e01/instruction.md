You are tasked with building a configuration history pipeline. We have a system that tracks the daily configuration settings for several internal applications. The raw data is exported daily into a wide-format CSV file, but our analytics team needs it in a normalized long format with rolling statistics to track configuration drift.

You need to build a pipeline with the following requirements:

1. **Input Data**: 
   A raw data file is located at `/home/user/raw_configs.csv`. 
   It has the following columns: `date,app1_workers,app1_threads,app2_workers,app2_threads`.
   (You must assume this file exists and contains time-series data sorted by `date`).

2. **Phase 1: Reshape (Wide to Long)**
   Write a Python script `/home/user/reshape.py` that reads `/home/user/raw_configs.csv` and converts it into a long-format CSV saved at `/home/user/long_configs.csv`.
   The output CSV must have exactly these columns: `date,app,metric,value`.
   For example, a column named `app1_workers` should map to `app="app1"` and `metric="workers"`.
   Sort the output by `date`, `app`, and `metric` in ascending order.

3. **Phase 2: Rolling Statistics**
   Write a Python script `/home/user/rolling.py` that reads `/home/user/long_configs.csv` and calculates a rolling 3-day mean for each `app` and `metric` combination.
   Save the output to `/home/user/rolling_stats.csv`.
   The output CSV must have the columns: `date,app,metric,value,rolling_mean`.
   - The data is daily, so a 3-period rolling window over rows (grouped by app and metric, sorted by date) is equivalent to a 3-day rolling mean.
   - Use a minimum number of periods of 1 (`min_periods=1`).
   - Round the `rolling_mean` to 2 decimal places.

4. **Phase 3: DAG Orchestration**
   Write a Python script `/home/user/pipeline.py` that acts as a simple DAG orchestrator. It must programmatically execute `/home/user/reshape.py` and then, only upon success, execute `/home/user/rolling.py`. If the first step fails, it should exit with a non-zero status code.

5. **Phase 4: Scheduling**
   Configure a cron job for the current user (`user`) that runs `/home/user/pipeline.py` using the standard Python 3 executable at the top of every hour (i.e., minute 0). 

After writing the scripts, execute `/home/user/pipeline.py` manually once so that the output files are generated.