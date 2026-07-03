You are tasked with building a high-performance C-based ETL and inference benchmarking pipeline. As a data scientist, you often deal with raw datasets where numeric columns contain missing data (like empty strings or "NaN"), which can silently corrupt data types or downstream calculations if not handled properly. 

Your objective is to write a C program that reads a raw dataset, cleans it by imputing missing values, performs inference using a predefined linear regression model, and benchmarks the inference performance.

Here are the specific steps you must implement:

1. **Dataset Parsing and ETL**:
   - Write a C program located at `/home/user/pipeline.c`.
   - The program must read an input CSV file at `/home/user/raw_data.csv`.
   - The CSV has four columns: `id` (integer), `f1` (integer), `f2` (string/mixed), and `target` (float).
   - Some entries in the `f2` column contain missing values represented as either an empty string `,,` or the string `NaN`. 
   - Compute the integer mean (truncated/floor) of all valid integer entries in the `f2` column.
   - Replace any missing or "NaN" values in `f2` with this computed integer mean.

2. **Inference and Export**:
   - Apply the following linear regression formula to calculate the `target` column for all rows:
     `target = (0.25 * f1) + (0.75 * f2)`
   - Export the cleaned and inferred dataset to `/home/user/cleaned_data.csv` in the exact same format (`id,f1,f2,target`), including the header. Format the `target` to exactly two decimal places.

3. **Inference Benchmarking**:
   - In the same C program, isolate the inference logic (the math operation `(0.25 * f1) + (0.75 * f2)`) and run it in a loop 10,000,000 times over the cleaned dataset arrays to benchmark its raw performance.
   - Measure the total wall-clock time taken for this 10,000,000-iteration loop in seconds.

4. **Summary Reporting**:
   - Create a summary text file at `/home/user/summary.txt` with the following format:
     ```
     Imputed_f2_Mean: <integer_value>
     Target_ID_2: <float_value_2_decimal_places>
     Target_ID_4: <float_value_2_decimal_places>
     Benchmark_Time_Sec: <float_value_6_decimal_places>
     ```

Compile your C program into an executable named `/home/user/pipeline` using `gcc` and run it to generate `/home/user/cleaned_data.csv` and `/home/user/summary.txt`. Do not use external libraries other than the C standard library.

Note: The environment already has `gcc` installed. We will place the `raw_data.csv` in `/home/user/` before your program runs.