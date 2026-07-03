You are a data scientist cleaning a dataset of sensor logs. You have a raw tab-separated values (TSV) file located at `/home/user/dataset.tsv`. The file has no header and contains four columns:
1. `LogID` (integer)
2. `SensorA_Reading` (float)
3. `Timestamp` (integer)
4. `SensorB_Reading` (float)

Your task is to compute the Pearson correlation coefficient between `SensorA_Reading` and `SensorB_Reading` across all rows in the dataset. 

Because of performance requirements for our ETL pipeline, you must implement the correlation calculation in C.
1. Write a C program and save it to `/home/user/corr.c`.
2. The C program should read pairs of double-precision floating-point numbers from standard input (stdin) until EOF, representing the two variables.
3. The program must compute the Pearson correlation coefficient. Make sure to use `double` for all internal summations to ensure numerical accuracy.
4. The program should print the final correlation coefficient to standard output (stdout), formatted to exactly four decimal places (e.g., `0.8524\n`).
5. Compile your program to `/home/user/corr`.
6. Use standard command-line tools (like `awk` or `cut`) to extract just the `SensorA_Reading` and `SensorB_Reading` columns from `/home/user/dataset.tsv`, pipe them into your compiled `./corr` program, and save the single resulting output value to `/home/user/result.txt`.

Ensure your C code handles the exact number of rows piped to it dynamically (do not hardcode the number of lines, though it will be less than 100,000).