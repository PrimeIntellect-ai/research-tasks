You are a data analyst responsible for large-scale data pipeline reproducibility. We have received a batch of sensor data in `/home/user/sensor_data.csv` that contains missing values and potential outliers. 

We use a proprietary, compiled imputation engine located at `/app/imputer`. We lost its source code, but it is known to be a command-line tool that takes an input CSV file and an output CSV file as arguments. It processes the dataset by filling in missing values in the numeric columns.

Your tasks are to:
1. Run the `/app/imputer` binary on `/home/user/sensor_data.csv` to generate a complete dataset at `/home/user/imputed.csv`. You may need to inspect the binary to understand its expected arguments.
2. Write a C program located at `/home/user/calc_metric.c` that parses a CSV file with the format `id,timestamp,value` (with a header row). 
3. Your C program must calculate the standard deviation of the `value` column from the parsed CSV, while implementing basic outlier handling: it must **completely ignore** any rows where `value` is less than 0.0 or greater than 1000.0.
4. Compile your C program and run it on `/home/user/imputed.csv`. 
5. Save the single resulting floating-point number (the standard deviation, formatted to at least 4 decimal places) into `/home/user/metric.txt`.

Ensure your C program is robust and correctly implements the standard sample standard deviation formula (using N-1). We will test your output against a reference implementation.