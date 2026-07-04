You are a data analyst optimizing a data pipeline. Our Python-based transformation script is too slow for our new scale, so we are migrating the core Extract-Transform-Load (ETL) pipeline to C.

Your task is to build this C-based ETL step, perform a linear algebra transformation on the data, and create a testing script to ensure reproducibility.

**Input Data:**
1. `/home/user/raw_data.csv`: A CSV file with headers `id,f1,f2,f3`. Each row contains an integer ID and three floating-point features.
2. `/home/user/transform.csv`: A 3x3 transformation matrix (comma-separated, no headers).

**Requirements:**

1. **Write the ETL code in C:** 
   Create a C program at `/home/user/etl.c`. 
   The program must read `raw_data.csv` and `transform.csv`. 
   For every row in `raw_data.csv`, you must multiply the feature vector `V = [f1, f2, f3]` by the 3x3 matrix `M` from `transform.csv` to compute a new vector `O = [out1, out2, out3]`.
   
   The exact math for the matrix multiplication (where `M[r][c]` is row `r`, col `c` of the matrix) is:
   `out1 = f1*M[0][0] + f2*M[1][0] + f3*M[2][0]`
   `out2 = f1*M[0][1] + f2*M[1][1] + f3*M[2][1]`
   `out3 = f1*M[0][2] + f2*M[1][2] + f3*M[2][2]`

2. **Output Formatting:**
   The C program should write the results to `/home/user/processed_data.csv`.
   The output must include the header `id,out1,out2,out3`.
   Format the floating-point outputs exactly to 4 decimal places (e.g., `%.4f`).
   
3. **Reproducibility Testing:**
   Write a bash script at `/home/user/test_pipeline.sh` that:
   - Compiles `/home/user/etl.c` into an executable named `/home/user/etl_bin` using `gcc` (with `-lm` if necessary).
   - Runs `/home/user/etl_bin`.
   - Checks if `/home/user/processed_data.csv` exists and contains exactly 4 lines (1 header + 3 data rows).
   - If successful, prints "PIPELINE PASS" to standard output. Otherwise, prints "PIPELINE FAIL".

**Execution:**
You must run your pipeline and ensure `/home/user/processed_data.csv` is generated correctly.