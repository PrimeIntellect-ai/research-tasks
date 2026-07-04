You are a data analyst working with a pipeline that processes high-frequency sensor data. Due to performance requirements, the core data processing step must be implemented in C. 

Your task is to write a C program that reads a dataset, cleans it, calculates statistics using the GNU Scientific Library (GSL), and aggregates the results into a summary CSV.

Here is the specification:
1. **Input Data**: A CSV file located at `/home/user/sensor_data.csv`. It has a header row and four columns: `timestamp,sensor1,sensor2,sensor3`.
2. **Missing Values**: Some rows contain missing values (represented as empty strings, e.g., `,,`, or unparseable strings like `NaN`). You must completely discard any row that has an invalid or missing value for *any* of the three sensors.
3. **Outlier Detection (using GSL)**: 
   - First, compute the arithmetic mean and sample standard deviation of the `sensor1` column across all the clean rows (using GSL functions `gsl_stats_mean` and `gsl_stats_sd`).
   - Second, filter out any row where the `sensor1` value is strictly more than `2.0` standard deviations away from the mean (i.e., reject if `|sensor1 - mean| > 2.0 * sd`).
4. **Aggregation**: For the rows that remain after outlier removal, compute the arithmetic mean of `sensor2` and `sensor3`.
5. **Output**: Your C program must write the final results to `/home/user/summary.csv`. The file must contain exactly two lines (a header and the data values formatted to exactly 4 decimal places):
   ```csv
   valid_rows,sensor1_mean,sensor1_sd,sensor2_mean,sensor3_mean
   [integer],[float],[float],[float],[float]
   ```
   *Note: `valid_rows` is the number of rows remaining AFTER outlier removal. `sensor1_mean` and `sensor1_sd` should be the statistics calculated BEFORE outlier removal.*

**Deliverables**:
- Create `/home/user/process_sensors.c`.
- Create a `/home/user/Makefile` that compiles `process_sensors.c` into an executable named `process_sensors`, correctly linking against the GSL and math libraries (`-lgsl -lgslcblas -lm`).
- Create a bash script `/home/user/run.sh` that builds the program using your Makefile and executes it.

*Ensure your code handles typical CSV parsing edge cases in C, such as trailing newlines. You may install the GSL development headers via `sudo apt-get update && sudo apt-get install -y libgsl-dev` if they are not present.*