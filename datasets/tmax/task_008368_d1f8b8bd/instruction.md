You are a data scientist tasked with cleaning a messy dataset of sensor readings using a high-performance ETL step. You need to write a C program to process the data, link the necessary mathematical libraries, and track the experiment's results.

The raw data is located at `/home/user/raw_data.csv`. It has two columns: `id,measurement`.
Some of the measurements contain invalid data such as `NaN`, `Infinity`, `-Infinity`, or negative values (which are physically impossible for this sensor).

Your task:
1. Write a C program at `/home/user/etl_clean.c`.
2. The program must read `/home/user/raw_data.csv`.
3. It should filter out any rows where `measurement` is:
   - Not a Number (NaN)
   - Infinity or -Infinity
   - Less than 0.0
4. Write the valid rows (including the `id,measurement` header) to a new file at `/home/user/clean_data.csv`. The `measurement` should be printed to 1 decimal place.
5. Calculate the sample mean and the sample variance of the valid measurements.
6. Track this ETL experiment by writing the summary statistics to a JSON file at `/home/user/run_metrics.json`. The JSON should have exactly this structure:
   ```json
   {
     "valid_count": <integer>,
     "mean": <float_to_4_decimal_places>,
     "sample_variance": <float_to_4_decimal_places>
   }
   ```
7. Compile your C program to an executable named `/home/user/etl_clean`. Be sure to configure the build to properly link the standard numerical/math library required for the `isnan()` and `isinf()` checks.
8. Run the executable to produce the output files.