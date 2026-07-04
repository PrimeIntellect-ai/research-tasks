You are a data engineer tasked with building a high-performance ETL pipeline for time-series sensor data. 

We use a specific version of GNU Parallel for parallel data processing, which has been pre-vendored on your system at `/app/parallel-20231022`. However, the deployment of this package failed during setup because of a deliberate configuration error introduced by a rogue commit.

Your tasks are:
1. **Fix the vendored package:** Identify and fix the perturbation in the GNU Parallel source code located at `/app/parallel-20231022`. Ensure that you can successfully run `/app/parallel-20231022/src/parallel`.
2. **Build the ETL Script:** Write a Bash script at `/home/user/etl.sh` that reads time-series data from standard input (stdin) and outputs aggregated results to standard output (stdout).
3. **Data Processing Requirements:**
   - The input is a headerless CSV stream with three columns: `timestamp,sensor_id,value` (e.g., `1700000010,TEMP_01,45`).
   - **Sampling/Stratification:** You must filter the stream to keep *only* the rows where the `timestamp` is exactly divisible by 10 (i.e., `timestamp % 10 == 0`).
   - **Aggregation:** Group the filtered records by `sensor_id`.
   - **Computation:** For each `sensor_id`, calculate the sum of the `value`s and the total count of sampled readings.
   - **Orchestration:** You must use the fixed GNU Parallel (`/app/parallel-20231022/src/parallel`) within your script to parallelize the aggregation or filtering step (e.g., processing chunks or distinct sensors in parallel).
   - **Output Format:** A headerless CSV in the format `sensor_id,total_value,sample_count`. The output must be sorted alphabetically by `sensor_id`.

Your script `etl.sh` must be robust and produce bit-exact deterministic output. An automated test suite will fuzz your script with thousands of random CSV inputs and compare its standard output to a verified oracle.

Example Input:
1700000000,S01,10
1700000005,S01,20
1700000010,S02,5
1700000010,S01,15

Example Output:
S01,25,2
S02,5,1