You are acting as a systems data scientist. Your task is to set up a robust, parallelized data cleaning pipeline in C that processes sensor datasets, imputes missing values, and runs on a scheduled basis.

We have provided a vendored copy of `libcsv-3.0.3` located at `/app/libcsv-3.0.3`. However, the provided source code has a broken configuration (specifically, its Makefile is misconfigured). 

Your tasks are:

1. **Fix and Build the Vendored Library**
   - Identify the deliberate perturbation in the `Makefile` of `/app/libcsv-3.0.3` and fix it.
   - Compile and install the library locally to `/home/user/local/` (ensure headers go to `/home/user/local/include` and shared/static libraries to `/home/user/local/lib`).

2. **Write the Imputation Tool in C**
   - Create a C program at `/home/user/imputer.c` and compile it to `/home/user/imputer`.
   - The program must take a single command-line argument: the path to an input CSV file.
   - The CSV format is strictly two columns: `timestamp,value` (e.g., `1600000000,15.5`). There is no header row. The timestamp is a 64-bit integer (`long long`), and the value is a double-precision float.
   - Missing data in the `value` column is represented by either an empty field (e.g., `1600000005,`) or the string `NaN`.
   - **Interpolation Rules**: 
     - Replace missing values using strict linear interpolation between the nearest previous and next valid values.
     - If missing values occur at the very beginning or end of the file, carry forward/backward the nearest valid value (constant extrapolation).
   - **Parallel Processing**: You must parallelize the imputation pass over the data array using OpenMP (`#pragma omp parallel for` or similar chunking strategies). You may load the entire file into memory first, as files will not exceed 100MB.
   - Use the locally installed `libcsv` to parse the files.
   - Output the cleaned data to `stdout` in the exact format: `%lld,%.6f\n`.

3. **Create a Pipeline and Cron Schedule**
   - Write a shell script at `/home/user/pipeline.sh` that iterates over all `.csv` files in `/home/user/incoming/`, runs `/home/user/imputer` on each, redirects the output to `/home/user/processed/` (keeping the same filename), and then removes the original file from `incoming`.
   - Ensure the script is executable.
   - Create a cron configuration file at `/home/user/pipeline.cron` that schedules `/home/user/pipeline.sh` to run exactly every 5 minutes.

Your C program must be bit-exact in its output compared to our reference implementation, which will be tested against thousands of dynamically generated edge cases.