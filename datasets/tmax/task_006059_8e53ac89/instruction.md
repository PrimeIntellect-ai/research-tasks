You are an engineer building an ETL pipeline. We need a highly performant C-based step to filter sensor data, but our initial environment is completely bare.

Your task is to set up the analysis environment, write a C program utilizing the GNU Scientific Library (GSL), and wrap it in a bash script to ensure pipeline reproducibility.

**Requirements:**

1. **Environment Setup:**
   - Install the necessary C compiler and GSL (GNU Scientific Library) development headers and libraries. 

2. **C Program (`/home/user/etl_filter.c`):**
   - Write a C program that reads a binary input file containing 10,000 `double` (8-byte, little-endian IEEE 754) values.
   - The program must use GSL's statistics functions (specifically `gsl_stats_mean` and `gsl_stats_sd` to compute the sample standard deviation) to calculate the mean and standard deviation of the dataset.
   - It should iterate over the dataset and write *only* the values that fall within `[mean - 2.0 * sd, mean + 2.0 * sd]` to a new binary file.
   - The program must take two command-line arguments: the input file path and the output file path.
   - The program must print exactly three lines to standard output:
     `Mean: <mean>` (formatted to 6 decimal places)
     `SD: <sd>` (formatted to 6 decimal places)
     `Count: <count>` (integer, representing the number of values that passed the filter)

3. **Pipeline Wrapper (`/home/user/run_pipeline.sh`):**
   - Create a bash script that:
     1. Compiles `/home/user/etl_filter.c` into an executable named `etl_filter`. Ensure you link the GSL and math libraries (`-lgsl -lgslcblas -lm`).
     2. Runs the compiled executable using `/home/user/input_data.bin` as the input and `/home/user/output_data.bin` as the output.
     3. Captures the standard output of the C program and saves it to `/home/user/pipeline_metrics.txt`.
   - Make sure `/home/user/run_pipeline.sh` is executable.

You must execute `/home/user/run_pipeline.sh` successfully before finishing the task.
The input file `/home/user/input_data.bin` has already been generated for you.