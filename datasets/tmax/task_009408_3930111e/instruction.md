You are an ML Engineer preparing training data for a new model. The raw data pipeline dumps a daily CSV file that is often corrupted with invalid types and out-of-bounds values. You need to build a fast, reproducible pipeline step using C++ to enforce a strict data schema.

Your task:
1. Write a C++ program at `/home/user/cleaner.cpp` that reads a CSV file from standard input (`stdin`) and writes valid rows to standard output (`stdout`).
2. The input CSV has no header. Each row is separated by a newline (`\n`) and columns are separated by exactly one comma (`,`).
3. The expected schema for the 4 columns is:
   - Column 1 (`id`): Integer. Must be strictly greater than 0.
   - Column 2 (`score`): Float. Must be between 0.0 and 100.0 (inclusive).
   - Column 3 (`category`): String. Must not contain commas, and the length must be between 1 and 10 characters (inclusive).
   - Column 4 (`is_active`): Boolean. Must be exactly the character '0' or '1'.
4. If a row does not exactly match this schema, drop it completely (do not print it). Do not print any error messages to stdout.
5. Write a bash script at `/home/user/run_pipeline.sh` that makes the pipeline reproducible. The script should:
   - Compile `/home/user/cleaner.cpp` using `g++ -O3 -std=c++17 -o /home/user/cleaner`.
   - Run the compiled executable, piping the contents of `/home/user/raw_data.csv` into it.
   - Redirect the valid output to `/home/user/clean_data.csv`.

Make sure `/home/user/run_pipeline.sh` is executable (`chmod +x`). 
Run your pipeline script to produce `/home/user/clean_data.csv` so it can be verified.