You are a data engineer building a lightweight ETL pipeline in C to process sensor readings.

We have a raw dataset located at `/home/user/sensor_data.csv` containing two columns: `timestamp` and `temperature`. The data is messy: some `temperature` values are missing (empty strings), and some are extreme outliers due to sensor malfunction (e.g., values > 100.0 or < -50.0).

We rely on a proprietary third-party C library for our statistical analysis, vendored at `/app/libstatboot-1.2`. This library provides a highly optimized `double compute_bootstrap_mean(double* data, int n, int num_samples)` function.

However, the vendored package has a broken build configuration, and the pipeline needs to be assembled.

Your task is to:
1. Navigate to `/app/libstatboot-1.2` and fix the build configuration. There is a deliberate error in the `Makefile` preventing it from compiling the shared library `libstatboot.so`.
2. Write a C program at `/home/user/etl_pipeline.c` that does the following:
   - Reads `/home/user/sensor_data.csv`.
   - Filters out rows where the `temperature` is missing.
   - Filters out outliers (keep only rows where -50.0 <= temperature <= 100.0).
   - Collects the cleaned temperature values into an array.
   - Links against the fixed `libstatboot.so`.
   - Calls `compute_bootstrap_mean(data, valid_count, 10000)` using the cleaned array.
   - Writes the resulting double value to `/home/user/bootstrap_result.txt` formatted to 4 decimal places.

To complete the task:
- Compile your C program successfully, ensuring it correctly links the shared library (you may need to set `LD_LIBRARY_PATH` when running it).
- Run your pipeline so that `/home/user/bootstrap_result.txt` is created with the final computed bootstrap mean.