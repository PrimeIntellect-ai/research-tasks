You are a data analyst working with a daily sales export from a legacy system. 

You have been provided with a raw CSV file located at `/home/user/raw_sales.csv`. 
However, this file has a few quirks:
1. It is encoded in `ISO-8859-1`, not UTF-8. The file contains a `Currency` column with special characters (like the `£` symbol) that will look garbled if not handled correctly.
2. The rows are completely out of order.

The columns in the input file are: `StoreID,Date,SalesAmount,Currency` (where `Date` is in `YYYY-MM-DD` format).

Your objective is to process this file and compute a rolling statistic using standard Linux command-line tools and a custom C program.

Please complete the following steps:
1. Use standard bash utilities to convert the `raw_sales.csv` file from `ISO-8859-1` to `UTF-8`. Save the converted file as `/home/user/utf8_sales.csv`.
2. Write a C program named `/home/user/process_sales.c` that reads `utf8_sales.csv`.
3. Your C program must:
   - Parse the CSV data (skipping the header).
   - Group the records by `StoreID`.
   - Sort the records within each group chronologically by `Date` (ascending). If dates are equal, preserve the original relative order.
   - Compute a 3-day rolling average of the `SalesAmount` for each `StoreID`. The 3-day rolling average for a given date should include the `SalesAmount` of that date and the up to 2 strictly preceding available dates in the sorted list for that store. (If it's the first day for a store, the average is just that day's amount. If it's the second day, it's the average of the first and second days).
   - Ignore the `Currency` column in the output, but ensure your parser doesn't break when encountering it.
4. The C program must output the results to `/home/user/rolling_sales.csv` with the following exact CSV format (including this header):
   `StoreID,Date,SalesAmount,RollingAvg`
   - `RollingAvg` must be formatted as a floating-point number with exactly 2 decimal places (e.g., `150.50`).
5. Compile your C program using `gcc` and run it to generate the final `rolling_sales.csv`.

Ensure your C program is robust and handles memory correctly. Do not use external C libraries other than the standard C library (`libc`).