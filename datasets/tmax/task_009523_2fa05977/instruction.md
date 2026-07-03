You are acting as a data engineer maintaining an ETL pipeline. 

We have a fast C-based data filter step in our pipeline located in `/home/user/etl_pipeline`. It reads a CSV from standard input, filters rows where `value > 20.0`, and prints the result to standard output. 

However, downstream models have been failing because of a silent data corruption issue. Large 64-bit integer IDs in the CSV are inexplicably having their last few digits altered (e.g., precision loss), resembling an issue where integers are silently cast to lower-precision floating-point numbers during parsing.

Your tasks are:
1. Inspect the C source code `/home/user/etl_pipeline/filter.c`. Identify and fix the bug causing the `id` field to lose precision. The `id` field must be accurately read and output as a 64-bit unsigned integer (`uint64_t`).
2. Recompile the program using the provided `Makefile` by running `make`.
3. Process the raw data by piping `/home/user/etl_pipeline/data.csv` into `./filter` and redirecting the output to `/home/user/etl_pipeline/output.csv`.
4. Validate your pipeline's output by running the provided validation script: `python3 validate.py output.csv > validation.log`.

The final state must contain the corrected `filter.c`, the generated `output.csv` with uncorrupted IDs, and a `validation.log` file containing the word "PASS".