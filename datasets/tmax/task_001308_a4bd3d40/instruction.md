You are a data engineer tasked with building a high-performance, reproducible ETL pipeline using C. You need to process a raw batch of sensor data, strictly enforce a data schema, separate valid from invalid records, and build a reproducibility test.

Your tasks are to:

1. **Write the ETL Processor in C**:
   Create a file at `/home/user/etl_processor.c`. The program should:
   - Read a CSV file named `/home/user/raw_data.csv` (which will be present).
   - Parse each line. The expected schema is 3 columns separated by commas:
     - Column 1: `id` (integer). Must be greater than 0.
     - Column 2: `status` (string). Must be exactly "ACTIVE" or "INACTIVE".
     - Column 3: `value` (float). Must be a valid floating-point number.
   - If a row successfully parses and meets all schema conditions, write it to `/home/user/clean_data.csv` in the format `%d,%s,%.2f\n` (e.g., `1,ACTIVE,10.50`).
   - If a row fails parsing or violates the schema, write the *exact original line* (including its newline) to `/home/user/rejected.log`.
   - Ensure the program gracefully handles the end of the file.

2. **Create a Makefile**:
   Create `/home/user/Makefile` to build the ETL pipeline.
   - The default target (`all`) should compile `etl_processor.c` into an executable named `etl_processor` using `gcc` with `-O2 -Wall`.
   - Include a `clean` target that removes the executable, `clean_data.csv`, and `rejected.log`.

3. **Build a Pipeline Reproducibility Test**:
   Create a bash script at `/home/user/test_pipeline.sh`. The script must:
   - Run `make clean` and `make`.
   - Run `./etl_processor`.
   - Compute the `md5sum` of `/home/user/clean_data.csv`.
   - Run `make clean`, `make`, and `./etl_processor` a second time.
   - Compute the `md5sum` of `/home/user/clean_data.csv` again.
   - Compare the two checksums. If they match, print "REPRODUCIBLE" and exit with code 0. If they do not match, exit with code 1.
   - Make sure `/home/user/test_pipeline.sh` is executable.

You may run any terminal commands necessary to write, compile, and test your code.