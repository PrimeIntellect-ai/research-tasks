You are an AI assistant helping a data science researcher organize a massive dataset of IoT sensor logs. The researcher needs a highly optimized C-based inference tool to filter out corrupted or anomalous "evil" data points before they are ingested into the primary database.

You have three main objectives:

1. **Fix the Vendored Dependency**
   We are using a fast CSV parsing library, `libfastcsv` (version 0.9.3), located at `/app/libfastcsv-0.9.3`. However, the library currently cannot be built. The researcher suspects there is a deliberate perturbation or configuration error in its `Makefile` preventing compilation. Fix the build system so you can run `make` and produce the static library `libfastcsv.a`.

2. **Hyperparameter Tuning & Cross-Validation**
   The researcher has provided a labeled dataset of sensor readings at `/home/user/train_sensor_data.csv`. The file has three columns: `sensor_alpha` (float), `sensor_beta` (float), and `is_anomaly` (integer: 0 for clean, 1 for evil). 
   You must perform a quick analysis (you can use Python, R, or any command-line tools) using cross-validation to find a linear decision boundary (e.g., `w1 * sensor_alpha + w2 * sensor_beta > threshold`) that perfectly separates the clean data from the anomalies.

3. **Develop the C Inference Tool and Benchmark**
   Write a C program at `/home/user/filter.c` that:
   - Includes and uses the fixed `libfastcsv` library to parse an input CSV file. The CSV file will only contain `sensor_alpha` and `sensor_beta` columns (no labels).
   - Applies the decision boundary you found in step 2.
   - If *any* row in the CSV file violates the boundary (i.e., is classified as an anomaly), the program should immediately print `REJECT` to standard output and exit.
   - If all rows are clean, it should print `ACCEPT` to standard output and exit.
   - Compile your program into an executable at `/home/user/run_filter`. 
   - Ensure the code runs extremely fast (benchmark your inference loop to process rows in minimal time, though no specific microsecond target is enforced, it must be compiled with `-O3`).

**CLI Contract for Verification:**
Your compiled binary must accept exactly one argument (the path to a CSV file) and output exactly `ACCEPT` or `REJECT`.
Example invocation: `/home/user/run_filter /path/to/data.csv`

Ensure your executable is completely self-contained and statically links to `libfastcsv.a`.