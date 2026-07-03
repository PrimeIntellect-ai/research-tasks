You are a data engineer tasked with building a high-performance ETL pipeline for IoT time-series data. You need to process raw sensor readings, anonymize sensitive user identifiers, and aggregate the results. 

To maximize performance, the core transformation must be written in C, and the pipeline orchestration must be managed using `make`, which natively handles Directed Acyclic Graphs (DAGs) and parallel execution.

**Your Objectives:**

1. **Create the Transformation Engine (C):**
   Write a C program at `/home/user/etl_pipeline/masker.c` that reads comma-separated values from `stdin` and writes the transformed data to `stdout`.
   - The input data has no headers. Each line follows this format: `Timestamp,SensorID,UserID,Value` (e.g., `2023-10-01T10:00:00,SENSOR_A,USER_123,22.5`).
   - You must mask the `UserID` (the 3rd column) using the DJB2 hash algorithm to ensure anonymization.
   - The output must be exactly the same as the input, but with the `UserID` replaced by its DJB2 hash represented as an 8-character lowercase hexadecimal string (e.g., `%08x`).
   - Leave the other columns completely unmodified.
   - **DJB2 Algorithm details:**
     ```c
     unsigned int djb2(const char *str) {
         unsigned int hash = 5381;
         int c;
         while ((c = *str++)) {
             hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
         }
         return hash;
     }
     ```

2. **Orchestrate the Pipeline DAG (Makefile):**
   Create a `Makefile` at `/home/user/etl_pipeline/Makefile`.
   The pipeline must process three raw data files located at `/home/user/etl_pipeline/raw/raw_data1.csv`, `raw_data2.csv`, and `raw_data3.csv`.
   Your `Makefile` must define the following targets to build the DAG:
   - `masker`: Compiles `masker.c` into an executable named `masker` using `gcc -O3`.
   - `masked/raw_data1.csv`, `masked/raw_data2.csv`, `masked/raw_data3.csv`: These targets must run the `masker` executable, taking the respective file from `raw/` as standard input and writing standard output to a new directory `/home/user/etl_pipeline/masked/` (your Makefile should create this directory if it doesn't exist). These tasks must be independent so they can run in parallel.
   - `aggregate.csv`: Depends on the three masked CSV files. It must concatenate them in order (1, then 2, then 3) into `/home/user/etl_pipeline/aggregate.csv`.
   - `all`: The default target, which depends on `aggregate.csv`.

3. **Execute the Pipeline:**
   Once built, run your pipeline using `make -j4 all` inside `/home/user/etl_pipeline/` to ensure the files are processed in parallel according to your DAG dependencies.

**Constraints:**
- Do not use any external libraries in C other than standard libc headers (`stdio.h`, `string.h`, `stdlib.h`).
- Ensure memory safety and handle lines of up to 1024 characters.
- The directory `/home/user/etl_pipeline/raw/` and the raw data files already exist.