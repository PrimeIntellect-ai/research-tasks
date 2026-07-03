I am a data analyst trying to process a large CSV dataset containing transaction records. I want to calculate the 95% confidence interval and standard error of the mean for the `amount` column using bootstrap resampling. 

I was given a fast, lightweight C library for CSV parsing called `fastcsv`, which is located in `/app/fastcsv-1.0/`. However, whenever I try to use it to read the `amount` column from my dataset at `/home/user/data/sales.csv`, the parsed values always come out as zero or blank. I suspect there is a misconfiguration or limitation in the library's source code preventing it from reading beyond the first few columns.

Please do the following:
1. Investigate the `fastcsv` library source in `/app/fastcsv-1.0/` and fix the issue that prevents it from parsing all columns of my CSV (my dataset has 5 columns: `id`, `timestamp`, `user_id`, `amount`, `category`). 
2. Recompile and install the library (a `Makefile` is provided in the directory).
3. Write a C program at `/home/user/bootstrap.c` that uses this library to read all rows from `/home/user/data/sales.csv`.
4. Implement a bootstrap sampling algorithm in your C program to estimate the standard error of the mean for the `amount` column. You must perform exactly 10,000 bootstrap resamples. For random number generation, seed your generator with `srand(42)` to ensure stability, though the verifier will allow for a small tolerance.
5. Compile and run your program.
6. Write the final results to `/home/user/bootstrap_results.txt`. The file must contain exactly two lines in this format:
   Sample Mean: [calculated_mean]
   Standard Error: [calculated_se]

Ensure your C code is efficient and handles the memory limits appropriately. The dataset contains roughly 50,000 rows.