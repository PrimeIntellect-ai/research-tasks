You are tasked with fixing a silent data corruption bug in an ETL pipeline written in C. 

A previous data scientist wrote a C program, `/home/user/etl_processor.c`, to process a large dataset located at `/home/user/dataset.csv`. The CSV has a header and three columns: `id`, `val1`, and `val2`. The C program reads this CSV from standard input (ignoring the header), multiplies `val1` and `val2`, and outputs `id,product`.

However, the pipeline has a silent corruption issue similar to pandas silently casting integers to floats and injecting NaNs, but in reverse: missing values in our dataset are represented by the string `"NA"`. The standard `atoi()` function in C silently converts `"NA"` to `0`. Consequently, missing values are falsely outputting a product of `0`, corrupting the downstream model outputs.

Your task:
1. Modify `/home/user/etl_processor.c` so that if either `val1` or `val2` is exactly `"NA"`, the output product for that row should also be `"NA"` (e.g., `id,NA`).
2. The program should otherwise correctly multiply valid integer strings.
3. Compile your fixed program to `/home/user/etl_processor` using `gcc`.
4. Run the compiled program on `/home/user/dataset.csv` and save the standard output to `/home/user/processed.csv`. Make sure your C program or your shell pipeline skips the CSV header row (`id,val1,val2`) so it doesn't try to parse the header as integers.

Output requirements:
- `/home/user/processed.csv` must contain the resulting rows in the format `id,result\n`.
- The number of lines in `/home/user/processed.csv` should perfectly match the number of data rows in `/home/user/dataset.csv` (total lines minus 1 for the header).